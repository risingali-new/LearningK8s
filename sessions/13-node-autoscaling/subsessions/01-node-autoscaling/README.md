# Sub-Session 01: Node Autoscaling

This sub-session shows what happens after HPA creates more Pods than the cluster can schedule.

HPA, VPA, and Deployments do not create Nodes.

If there is not enough node capacity:

```text
Pods stay Pending.
Scheduler emits FailedScheduling events.
Node autoscaler watches unschedulable Pods.
Node autoscaler adds capacity.
Scheduler places the Pods.
```

## Three EKS Node Scaling Options

### EKS Auto Mode

EKS Auto Mode is the most managed path. AWS manages compute autoscaling, core networking, load balancing integration, and storage drivers. If a Pod cannot fit on existing Auto Mode Nodes, EKS Auto Mode can create a new Node.

### Karpenter

Karpenter is a flexible autoscaler that watches unschedulable Pods and creates right-sized Nodes based on Pod requirements such as CPU, memory, instance type constraints, zones, taints, and affinities.

### Cluster Autoscaler

Cluster Autoscaler works with node groups backed by Auto Scaling Groups. It changes the desired capacity of those groups when Pods cannot schedule or when Nodes are underutilized.

## Before The Lab

Check current node capacity:

```bash
kubectl get nodes
kubectl describe nodes | grep -A5 "Allocated resources"
```

Check whether a node autoscaler is present:

```bash
kubectl get pods -A | grep -E "karpenter|cluster-autoscaler"
kubectl get nodepools 2>/dev/null || true
```

## Generic Pending Pods Demo

This works on any cluster. It creates Pods with enough CPU requests to exceed a small cluster.

From `sessions/13-node-autoscaling`:

```bash
kubectl apply -f subsessions/01-resource-guardrails/
kubectl apply -f subsessions/01-node-autoscaling/01-pending-pods-inflate.yml
```

Watch:

```bash
kubectl get pods -n app-scaling-prod -l app=pending-pods-inflate -w
```

Check scheduling events:

```bash
kubectl describe pod -n app-scaling-prod -l app=pending-pods-inflate
kubectl get events -n app-scaling-prod --sort-by='.lastTimestamp'
```

If no node autoscaler is configured, some Pods may stay Pending.

If node autoscaling is configured, new Nodes should appear:

```bash
kubectl get nodes -w
```

Cleanup:

```bash
kubectl delete -f subsessions/01-node-autoscaling/01-pending-pods-inflate.yml --ignore-not-found
```

## EKS Auto Mode Demo

Use this only on an EKS Auto Mode cluster.

Apply:

```bash
kubectl apply -f subsessions/01-node-autoscaling/02-auto-mode-inflate.yml
```

Watch:

```bash
kubectl get nodepools
kubectl get nodes -w
kubectl get events -n app-scaling-prod --sort-by='.lastTimestamp'
```

The manifest includes:

```yaml
nodeSelector:
  eks.amazonaws.com/compute-type: auto
```

That asks EKS Auto Mode to place the workload on Auto Mode compute.

Cleanup:

```bash
kubectl delete -f subsessions/01-node-autoscaling/02-auto-mode-inflate.yml --ignore-not-found
```

## Cluster Autoscaler Checklist

Use Cluster Autoscaler when your EKS cluster uses managed or self-managed node groups backed by Auto Scaling Groups.

Production setup usually needs:

- A Cluster Autoscaler version that matches the Kubernetes minor version.
- IAM permissions through IRSA or EKS Pod Identity.
- Node group Auto Scaling Groups tagged for auto-discovery.
- Sensible node group min/max sizes.
- Similar instance shapes inside a mixed instance node group.

Required ASG discovery tags commonly include:

```text
k8s.io/cluster-autoscaler/enabled = true
k8s.io/cluster-autoscaler/<cluster-name> = owned
```

Useful checks:

```bash
kubectl -n kube-system logs deployment/cluster-autoscaler
kubectl get events -A --sort-by='.lastTimestamp'
aws autoscaling describe-auto-scaling-groups --region "$AWS_REGION"
```

Cluster Autoscaler changes Auto Scaling Group desired capacity. It does not create arbitrary instance types outside the configured node groups.

## Karpenter Checklist

Use Karpenter when you want fast, workload-aware, just-in-time compute provisioning.

Production setup usually needs:

- Karpenter installed with Helm.
- Controller IAM permissions.
- A NodeClass that describes AWS infrastructure.
- A NodePool that describes allowed instance requirements.
- Subnets and security groups discoverable by Karpenter.
- Interruption handling for Spot workloads.

Useful checks:

```bash
kubectl get nodepools
kubectl get nodeclaims
kubectl -n kube-system logs deployment/karpenter
kubectl describe nodepool <nodepool-name>
```

With Karpenter, Pending Pods are matched to NodePool requirements. Karpenter then creates NodeClaims and launches suitable EC2 instances.

### Optional Karpenter NodePool Example

The file below is a teaching example for a normal EKS cluster with Karpenter installed:

```text
03-karpenter-nodepool-example.yml
```

Before applying it, edit these values:

- `KarpenterNodeRole-demo-batch16a`
- `karpenter.sh/discovery: demo-batch16a`
- Availability zones if your cluster is not in `us-east-2`

Apply:

```bash
kubectl apply -f subsessions/01-node-autoscaling/03-karpenter-nodepool-example.yml
kubectl get nodepools
kubectl get ec2nodeclasses
```

Then create a workload that targets that NodePool:

```bash
kubectl apply -f subsessions/01-node-autoscaling/04-karpenter-inflate.yml
kubectl get nodeclaims -w
kubectl get nodes -w
```

Cleanup:

```bash
kubectl delete -f subsessions/01-node-autoscaling/04-karpenter-inflate.yml --ignore-not-found
kubectl delete -f subsessions/01-node-autoscaling/03-karpenter-nodepool-example.yml --ignore-not-found
```

## EKS Auto Mode Checklist

Use EKS Auto Mode when you want AWS to manage most cluster infrastructure operations.

Useful checks:

```bash
kubectl get nodepools
kubectl describe nodepool general-purpose
kubectl get nodes -L eks.amazonaws.com/compute-type
```

Built-in Auto Mode node pools include:

- `system`
- `general-purpose`

You can create custom NodePools when you need specific capacity types, zones, architectures, or instance families.

### Optional EKS Auto Mode Custom NodePool Example

The file below is a teaching example for an EKS Auto Mode cluster:

```text
05-auto-mode-nodepool-example.yml
```

It references the built-in Auto Mode NodeClass:

```yaml
nodeClassRef:
  group: eks.amazonaws.com
  kind: NodeClass
  name: default
```

Apply:

```bash
kubectl apply -f subsessions/01-node-autoscaling/05-auto-mode-nodepool-example.yml
kubectl get nodepools
kubectl describe nodepool auto-training
```

Then target it with a workload:

```bash
kubectl apply -f subsessions/01-node-autoscaling/06-auto-mode-custom-nodepool-inflate.yml
kubectl get nodes -L billing-team,eks.amazonaws.com/compute-type -w
```

Cleanup:

```bash
kubectl delete -f subsessions/01-node-autoscaling/06-auto-mode-custom-nodepool-inflate.yml --ignore-not-found
kubectl delete -f subsessions/01-node-autoscaling/05-auto-mode-nodepool-example.yml --ignore-not-found
```

## Cleanup And Cost Control

Always delete inflate workloads:

```bash
kubectl delete -f subsessions/01-node-autoscaling/01-pending-pods-inflate.yml --ignore-not-found
kubectl delete -f subsessions/01-node-autoscaling/02-auto-mode-inflate.yml --ignore-not-found
kubectl delete -f subsessions/01-node-autoscaling/04-karpenter-inflate.yml --ignore-not-found
kubectl delete -f subsessions/01-node-autoscaling/06-auto-mode-custom-nodepool-inflate.yml --ignore-not-found
```

Then watch scale-down:

```bash
kubectl get pods -n app-scaling-prod
kubectl get nodes -w
```

Node scale-down is intentionally slower than scale-up. Autoscalers wait to avoid deleting capacity that may be needed again immediately.

## Review Questions

1. Why do Pods become Pending?
2. Why does HPA not solve Pending Pods by itself?
3. What does Cluster Autoscaler change in AWS?
4. What does Karpenter create when it provisions capacity?
5. Why does EKS Auto Mode need the `eks.amazonaws.com/compute-type: auto` selector in the sample?
6. Why should scale-down be slower than scale-up?
7. What cost risk appears if you forget to delete an inflate workload?
