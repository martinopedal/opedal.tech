---
title: "AKS Automatic in production: what you keep, what you wrap"
description: "Node provisioning, networking constraints, and the platform team responsibilities that don't disappear when AKS goes automatic."
pubDate: 2025-06-20
tags: ["Azure", "Kubernetes", "AKS", "PlatformEngineering"]
draft: true
---

AKS Automatic gets pitched as the version of AKS where the platform team can stop worrying about node pools. The pitch is mostly accurate. The parts where it is not accurate are the parts that matter most when you put real workloads on it.

Here is what I have kept, what I have wrapped, and what I would change before recommending it for a regulated landing zone.

## Karpenter is doing the heavy lifting

The node provisioning model in AKS Automatic is built on Karpenter, the same node autoprovisioner that came out of the AWS Kubernetes ecosystem and got upstreamed into the CNCF. In Azure, it shows up as the AKS Node Auto Provisioning feature, configured through `NodePool` and `AKSNodeClass` custom resources.

This part actually feels automatic. You deploy a pod with resource requests, Karpenter picks an appropriate VM SKU, provisions a node, schedules the pod, and tears the node down when the pod goes away. No predefined node pool with a fixed SKU. No "we need a GPU pool, please open a ticket" friction.

The fight starts at networking.

## Subnet sizing for ALZ Corp spokes

Karpenter node provisioning needs careful subnet sizing. The defaults assume more IP space than most ALZ Corp spoke VNets provide. In a typical landing zone subscription, the spoke VNet is a /22 or /23, the AKS node subnet is a /24, and the pod CIDR is overlay. That gives you 250 or so node IPs.

That sounds like a lot until Karpenter starts churning. During a deploy with rolling pod restarts and aggressive bin packing, you can easily be holding 30 to 40 node leases at once while old nodes drain and new ones come up. If you have multiple AKS clusters in the same spoke, you are out of IPs.

Settling pattern: ask for a /23 minimum on the node subnet for any cluster that runs more than 50 pods, and use Azure CNI overlay for pods so you do not also burn through pod IPs.

<!-- TODO: verify that Azure CNI overlay is the default in current AKS Automatic clusters. I think it is, but I want to confirm against the current default cluster definition. -->

## Taints, tolerations, and the workloads you do not want on demand-billed nodes

Automatic provisioning does not mean automatic billing tier selection. By default Karpenter picks spot or on-demand based on its own scoring, but you may have workloads where spot is not acceptable (databases, anything stateful with a slow start) and others where it is mandatory (batch jobs that you do not want eating budget).

I tag NodePools with billing intent and use taints and tolerations to keep workloads on the right tier:

```yaml
apiVersion: karpenter.azure.com/v1beta1
kind: NodePool
metadata:
  name: spot-batch
spec:
  template:
    spec:
      requirements:
        - key: karpenter.azure.com/sku-family
          operator: In
          values: ["D", "E"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot"]
      taints:
        - key: workload
          value: batch
          effect: NoSchedule
```

Without this, you will eventually find a production database pod scheduled onto a spot node, get evicted at 3 in the morning, and spend the rest of the week explaining why "automatic" did not save you.

<!-- TODO: confirm the exact apiVersion and group for the Azure Karpenter NodePool CRD in current AKS Automatic. The upstream Karpenter API moved to v1 and Azure may or may not have followed. -->

## Ingress and egress policy still belongs to you

AKS Automatic ships with managed ingress (using Application Gateway for Containers or NGINX) and a default egress through a managed NAT gateway. Both of these are configurable, and both of them stop being acceptable the moment you have a regulated workload that needs all egress through the central firewall.

For ALZ Corp clusters, I disable the managed NAT gateway and force egress through the hub firewall using user defined routes on the cluster subnet. The cluster subnet UDR points 0.0.0.0/0 at the firewall private IP. The firewall has the AKS FQDN tag allow rule, plus any registry and image source you depend on.

This part is the same work you would do on a non-Automatic cluster. The Automatic part does not save you any time here. It just does not get in the way.

## Monitoring, cost tracking, and the platform team responsibility that does not disappear

Container Insights is on by default. So is Managed Prometheus. So is Managed Grafana, if you wire it up. That is more observability out of the box than I have ever gotten from a fresh AKS install.

What is not on by default is meaningful cost attribution. Karpenter will provision the most cost-effective VM family for the pod, but if you have ten teams sharing one cluster, you still need namespace-level cost tracking to know who is responsible for the bill. Azure Cost Management does not give you that out of the box for AKS. OpenCost does. I install it on every cluster.

<!-- TODO: I want to add a note here about the new Azure-native cost allocation features for AKS that came out recently. I have not used them in production yet, so I do not want to make claims I cannot back up. -->

## Disaster recovery is still your job

Automatic does not back up your etcd. It does not snapshot your persistent volumes. It does not give you a tested restore procedure. You still need Velero or an equivalent, you still need to test the restore at least quarterly, and you still need to document the RTO and RPO commitments to the application teams.

This is the part that most teams forget when they hear "managed Kubernetes." Managed control plane is not the same as managed disaster recovery. Microsoft will keep your API server up. Microsoft will not restore your application state if you delete the wrong namespace.

## Identity and RBAC

Workload identity is on by default in Automatic. Use it. Federate the service accounts to user assigned managed identities and stop putting service principal secrets in `Secret` resources. This is the single biggest security improvement you can make on an AKS cluster, and Automatic makes it the default path instead of an opt-in.

Cluster RBAC integrates with Entra ID. Use group-based access, not direct user assignments. Pair it with Conditional Access for any cluster that runs production workloads.

## What actually feels automatic

The cluster upgrade story. Node image upgrades happen on schedule. Control plane upgrades happen on schedule. Nodes drain and reschedule pods cleanly. I have not had to manually trigger a node upgrade on an Automatic cluster in months.

Karpenter scaling is genuinely better than the cluster autoscaler. Right-sized nodes, fast provisioning, no overprovisioning of expensive node pools you might need someday.

Default observability is solid. The dashboards are not great, but the data is there.

## What I would change

Make the default egress configuration honest about regulated environments. The current default works for greenfield public-internet workloads. It does not work for ALZ Corp. Document the wrap pattern explicitly in the AKS Automatic docs, instead of treating it as advanced configuration.

If you have run AKS Automatic against a Corp landing zone, I am curious where you put the wrapper. Most of the teams I work with put it in their AKS Terraform module. A smaller number put it in a separate platform-team layer. Both work. The choice probably says more about the team structure than the technology.
