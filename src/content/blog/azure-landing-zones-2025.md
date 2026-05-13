---
title: "Azure Landing Zones in 2025: What's Changed"
description: "ALZ has matured significantly. Here's what the Corp reference architecture looks like today and the checklist automation that keeps it honest."
pubDate: 2025-03-15
tags: ["Azure", "Landing Zones", "Terraform", "IaC"]
---

Azure Landing Zones have been around long enough now that the patterns are well-established, but the tooling keeps evolving. Here's a current-state look at what a Corp deployment actually involves, and the automation layer that makes ongoing compliance tractable.

## What "Corp" means in practice

The Corp reference architecture is the one most enterprises should be running: management group hierarchy, centralized networking (hub-and-spoke or Virtual WAN), centralized logging, and a policy framework that enforces baseline controls across all subscriptions.

What it doesn't tell you is how to validate that what you deployed matches what the reference architecture says you should have deployed. That's where the checklist comes in.

## The ALZ Checklist problem

The official ALZ Checklist has over 200 items. Before I started working on `alz-graph-queries`, only about 49 of them were automatable via Azure Resource Graph. The rest required manual portal inspection.

That's not sustainable. A 200-item checklist that requires 150+ manual steps will be done once at deployment time and never again. It doesn't matter how good your policy definitions are if you're not continuously verifying the baseline.

## What we built

The `alz-graph-queries` repo covers 135 of those checklist items with Azure Resource Graph queries. The queries run against your entire tenant and return pass/fail for each item.

Plugged into `azure-analyzer`, these run on a schedule and produce a unified JSON + HTML report. The report goes into a storage account. A Logic App sends a digest to a Teams channel when the failure count changes.

The result is a landing zone that tells you when it drifts from baseline, not one you have to inspect manually.

## The Terraform side

On the IaC side, I maintain Terraform modules built specifically to deploy inside a Corp landing zone. The constraints matter:

- **No public IPs.** All egress through the central firewall.
- **Managed identity everywhere.** No service principal passwords in state files.
- **Private endpoints only.** No storage accounts or key vaults with public network access.
- **PSRule in CI.** Every plan runs through PSRule for Azure before apply.

These aren't optional constraints you configure away. They're defaults with no override. If a resource genuinely needs a public IP (rare), that's a conscious architectural decision that requires an explicit parameter and a comment explaining why.

## What's coming

The parts of the checklist that aren't automatable yet are mostly in the identity and governance space: Entra ID settings, PIM configuration, and break-glass account setup. Some of these can be automated via Microsoft Graph. I'm working on that layer now.

If you're running an ALZ deployment and want to know where you stand against the checklist, the `azure-analyzer` tool is the fastest way to find out. It runs in a container, needs read-only access to your tenant, and produces output in under ten minutes.
