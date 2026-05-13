---
title: "AI Foundry agent setup: Standard vs Basic and the SMI gotcha"
description: "Capability host, thread storage, vector store, and the managed identity configuration that breaks Standard Agent Setup for enterprise accounts."
pubDate: 2025-06-25
tags: ["Azure", "AIFoundry", "AI", "Microsoft"]
draft: true
---

The first AI Foundry agent I deployed to a regulated tenant failed at the capability host creation step. The deployment succeeded for the AI Foundry account. It succeeded for the project. It even succeeded for the AI Search and Cosmos DB connections. Then the capability host call returned a 403, and the deployment rolled back.

The root cause was not a missing role. It was a deny policy preventing the system-assigned managed identity on the AI Foundry account from being granted the role it needed on the connected resources.

That is the SMI gotcha. Here is what an agent actually is, what Standard Agent Setup does that Basic does not, and how to fix the SMI problem before it eats a deployment window.

## What an agent is, in plumbing terms

An AI Foundry agent is not a single resource. It is a composition of four things, all wired together through the AI Foundry project:

The **capability host**. This is the runtime that hosts the agent execution. It owns the lifecycle of agent invocations, tool calls, and threads. In Standard Agent Setup, the capability host is connected to your own storage backends. In Basic, it uses Microsoft-managed defaults that you cannot inspect.

The **thread storage**. Every agent conversation is a thread. The thread holds the message history, the system prompt, the tool call history. In Standard Agent Setup, the threads live in your Cosmos DB account. In Basic, they live in a Microsoft-managed store.

The **vector store**. Agents that use file search or knowledge retrieval need a vector index. In Standard Agent Setup, this is your Azure AI Search service. In Basic, it is a Microsoft-managed index that you cannot point at your own data sources.

The **connection**. The connection is the named binding between the AI Foundry project and an external resource (a model deployment, a storage account, an AI Search service). Connections carry the auth method (API key, managed identity, SAS) and the data they expose to the agent.

Once you understand that the agent is really four resources pretending to be one, the auth model makes more sense.

## Basic vs Standard Agent Setup

Basic Agent Setup is the demo path. You create an AI Foundry account, you create a project, you create an agent, and the platform handles thread storage and vector search for you using its own backends. It works in five minutes. It is not auditable, it is not portable, and it is not acceptable for any workload where data sovereignty matters.

Standard Agent Setup is the enterprise path. You bring your own Cosmos DB, your own Azure AI Search, and your own Storage account. The agent uses your resources, in your subscription, in your region, with your network controls. The data never leaves your tenant.

The difference matters more than the docs make it sound. With Standard Agent Setup, you can run the agent inside a privately networked AI Foundry account, with private endpoints on Cosmos DB and AI Search, and have a complete audit trail of every thread, every tool call, and every vector lookup. With Basic, you have a black box.

For any production deployment in a regulated environment, Standard Agent Setup is the only realistic option.

## The SMI gotcha

Here is where it breaks. Standard Agent Setup needs to grant role assignments from the AI Foundry account's managed identity to the connected Cosmos DB, AI Search, and Storage resources. Specifically:

- `Cosmos DB Built-in Data Contributor` on the Cosmos account
- `Search Index Data Contributor` and `Search Service Contributor` on the AI Search service
- `Storage Blob Data Contributor` on the Storage account

The Bicep or Terraform template that creates the AI Foundry account will, by default, enable a system-assigned managed identity (SMI) on the account. The capability host creation step then tries to grant the SMI those roles on the connected resources.

In an ALZ Corp environment, there is almost always a deny policy preventing automated role assignments. The most common variant is `Microsoft.Authorization/Deny-AA-Role-Assignment` or a custom variant of it that blocks any role assignment created outside of a privileged identity flow. The capability host creation hits that policy and returns a 403.

The error message is unhelpful. It says the capability host could not be created. It does not say "your deny policy blocked the role assignment for the system-assigned managed identity." You only figure that out by looking at the activity log on the connected resource and seeing the failed role assignment attempt.

<!-- TODO: confirm the exact policy definition name. I have seen it referenced as Deny-AA-Role-Assignment in ALZ docs and as a customer-named variant in several tenants. The defining behavior is the same but the name varies. -->

## The UMI fix

The fix is to switch from a system-assigned managed identity to a user-assigned managed identity (UMI). With a UMI, you create the identity first, you grant it the required roles up front (through whatever your privileged role assignment process is), and then you attach it to the AI Foundry account. The capability host creation no longer needs to create role assignments at deployment time, because the role assignments already exist.

```hcl
resource "azurerm_user_assigned_identity" "foundry" {
  name                = "id-foundry-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource "azurerm_role_assignment" "foundry_cosmos" {
  scope                = azurerm_cosmosdb_account.threads.id
  role_definition_name = "Cosmos DB Built-in Data Contributor"
  principal_id         = azurerm_user_assigned_identity.foundry.principal_id
}

# Repeat for AI Search and Storage roles before creating the AI Foundry account
```

<!-- TODO: confirm the exact role names. I have seen Cosmos DB Built-in Data Contributor referenced as both a built-in role and as a Cosmos data plane role. The data plane role is granted differently (through the SQL role assignment API, not Microsoft.Authorization), and I want to make sure the example does not conflate them. -->

## Account vs project level storage

One more wrinkle. AI Foundry lets you configure the connections at either the account level or the project level. Account level connections are inherited by all projects. Project level connections override the account level.

For a multi-team tenant where each team has its own project, project level is the right answer. Each team gets its own Cosmos DB and AI Search, isolated from other teams. The AI Foundry account is shared, but the data is not.

For a single-team tenant where you want everything to share the same backends, account level is fine and reduces the per-project setup work.

## Cosmos DB vs Azure AI Search: who does what

Cosmos DB stores threads. Every agent conversation, every message, every tool call. The data plane access pattern is heavy on writes and metadata reads. RU/s sizing matters. I usually start at 1000 RU/s autoscale and watch the metrics for the first month.

Azure AI Search stores the vector index for file search. Every uploaded file, chunked and embedded. The access pattern is heavy on read at agent invocation time. Replica count matters more than partition count for most agent workloads.

<!-- TODO: get the recommended starting tier for Azure AI Search in agent scenarios. I think Standard S1 with one replica is the floor, but I want to verify the official guidance and whether the new agentic tier changes the answer. -->

## Networking lockdown

Once the agent is working, lock down the network. Private endpoints on AI Foundry, Cosmos DB, and AI Search. Disable public network access on all three. The agent invocations from the application will go through the AI Foundry private endpoint, which routes the backend calls to the connected resources over the private network.

If you have a developer that says "but I cannot test the agent from my laptop now," that is the correct outcome. They should be testing through the application, not against the data plane directly.

## Cost implications

Standard Agent Setup is more expensive than Basic. You pay for Cosmos DB RU/s, you pay for AI Search SKU, you pay for the Storage account, and you pay for the model token usage on top of all of it.

For most enterprise scenarios, the cost difference is rounding error against the model token bill. It is also the only path to data residency, audit, and reproducibility, which means there is no real choice for production. Basic is for prototypes. Standard is for everything else.

## When to use which

Basic for the first week, when you are still figuring out whether the agent is going to do anything useful. Standard the moment you have a stakeholder who cares where the data lives.

If you hit the SMI gotcha, the error message will not tell you what is wrong. Check the connected resource activity logs first, and assume any deny policy on role assignments is the cause until proven otherwise.
