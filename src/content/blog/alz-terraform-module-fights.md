---
title: "Where ALZ Terraform module fights you (and how to settle it)"
description: "Subscription vending and management group enforcement patterns that work inside the constraints of the CAF Terraform module."
pubDate: 2025-06-15
tags: ["Azure", "Terraform", "ALZ", "LandingZones"]
draft: true
---

The first time you run the ALZ Terraform module against a tenant that already has a management group hierarchy, you find out very quickly that "greenfield" is not a suggestion. It is the assumption.

That is not a complaint. It is the design. The module assumes you are building the hierarchy, owning the policy assignments, and managing the subscriptions through it. The friction starts when reality does not match that assumption, and you still have to ship.

Here is what fights back, and how I have settled each one across the engagements where I have rolled the module out.

## subscription_id_overrides is doing more than you think

The `subscription_id_overrides` map looks like a simple lookup. You give it a management group key, you point it at one or more subscription IDs, and the module places those subscriptions in the right archetype.

What it actually does is move the subscription. Every time you run apply. If something else has moved the subscription out of band (a manual portal action, a lighthouse delegation, an Azure DevOps pipeline that has nothing to do with you), the next plan will reset it. That is correct behavior, but it surprises people the first time it happens during a Friday afternoon change window.

The settling pattern: lock down management group moves at the tenant root with a deny policy, document the override map as the single source of truth, and review it on every PR. If a subscription needs to move, it moves in code. Not in the portal.

```hcl
subscription_id_overrides = {
  "corp"    = ["00000000-0000-0000-0000-000000000001"]
  "online"  = ["00000000-0000-0000-0000-000000000002"]
  "sandbox" = ["00000000-0000-0000-0000-000000000003"]
}
```

## Management group hierarchy enforcement

The module wants to own the hierarchy from the intermediate root down. If you already have a hierarchy that does not match the ALZ archetypes, you have two choices: move the existing groups under the ALZ intermediate root and accept that your existing policy assignments will start fighting the ALZ ones, or build the ALZ hierarchy in parallel and migrate subscriptions over time.

I have done both. The parallel hierarchy is less painful for established tenants, even though it looks ugly in the portal for a few months. The reason is simple. Policy conflicts at the management group level are very hard to debug, and the ALZ assignments are dense. If you collide with an existing assignment that has the same definition but different parameters, you get a non-compliant resource that nobody will ever fix because nobody owns the conflict.

<!-- TODO: confirm the exact behavior when two management group scoped policy assignments with the same definition exist at different scopes. Last time I checked, the more specific scope wins, but I want to verify against the current docs. -->

## Policy assignment scope conflicts

This is where the module is opinionated in ways that bite hybrid environments. The ALZ default initiatives assume you are running fully cloud-native workloads with no on-prem dependencies. If you have a hub VNet that peers to ExpressRoute and carries traffic from a colocation facility, some of the network policies will flag legitimate flows.

The fix is not to disable the policies. The fix is to use policy exemptions, scoped to the specific resource group or subscription that has the legitimate exception, with an expiry date and a documented reason. Azure Policy supports time-bound, auditable exemptions natively. Most teams I work with have never configured one. They reach for `Disabled` on the assignment instead, which removes the control everywhere.

```hcl
resource "azurerm_management_group_policy_exemption" "expressroute_egress" {
  name                 = "expressroute-egress-exemption"
  management_group_id  = data.azurerm_management_group.connectivity.id
  policy_assignment_id = local.deny_public_endpoint_assignment_id
  exemption_category   = "Waiver"
  expires_on           = "2025-12-31T23:59:59Z"
  description          = "ExpressRoute hub requires controlled egress for legacy DR replication. Tracked in CHG-12345."
}
```

## State file size

The module produces a lot of resources. A baseline Corp deployment with three or four spokes and the default policy set will easily push your state file past 50 MB. That is fine for `terraform plan` on a workstation. It is not fine when you are running in a hosted runner with a 30 second timeout on the backend lock acquisition.

Split the state. I usually go with one state for the platform foundation (management groups, policies, role assignments at MG scope) and a separate state per landing zone subscription. The CAF module supports this pattern, but it requires you to wire the data sources between states explicitly. It is worth the extra plumbing.

<!-- TODO: confirm current state file size threshold where the AzureRM backend starts having latency issues. I have seen the slowdown around 50 MB but it may have improved with newer azurerm provider versions. -->

## Default policy parameters and hybrid reality

The default parameters for the ALZ initiatives assume that everything you deploy will use private endpoints, managed identity, and customer-managed keys. In a pure cloud-native shop, that is a reasonable default.

In a tenant that still has a SQL Server replication job from a 2017 server farm, those defaults will break workloads on day one. The settling pattern is to override the parameters for the specific initiatives you cannot meet yet, scoped to the specific landing zone that has the legacy dependency, with an explicit migration target date in the description field.

<!-- TODO: list the specific parameter names that I most often override. I think it is the customer-managed key requirement on Storage and the private endpoint requirement on SQL, but I want to check the current parameter names against the latest module version. -->

## Diagnostic settings per subscription

This is one of the things the module does well, but only if you give it the right Log Analytics workspace ID up front. If you bootstrap the platform without management subscription wiring, the diagnostic setting policy will assign but never remediate, and you will have empty workspaces with policy compliance showing green. That is the worst possible state. You think you have logging, and you do not.

Run a one-time remediation task after the module converges. Verify in the portal that at least one resource per subscription has an active diagnostic setting pointing at the correct workspace.

## RBAC pre-deployment validation

The module needs `Owner` on the tenant root group to do everything it claims to do. Most enterprises will not give that to a service principal. They will give you `Management Group Contributor` and tell you to deal with it.

You can deal with it. The role assignments at the tenant root are mostly for the deny assignments, which you can apply manually as a one-time elevated action and then drop the permission. Plan the elevation window, document it, and record what you did during the window. Then run the module with the lower permission.

<!-- TODO: write a small validation script that checks the calling identity has the required roles before running terraform apply. I have a draft of this for one customer but want to generalize it before publishing. -->

## What works without modification

Despite all of this, the parts that work straight out of the box are worth listing. The module gets the management group structure right. The policy initiative assignments are sensible. The Defender for Cloud configuration is solid. The connectivity subscription wiring with hub VNet, Bastion, and Firewall does not need any local overrides for most deployments.

When I review a landing zone now, the question is not "should we use the module." It is "where in the module do we deviate, and is each deviation documented." If you can answer the second question for every deviation, the module is doing its job.

If you have hit a different fight with the module that I have not covered, I am curious which one. Most of these patterns came from settling a single bad week of debugging.
