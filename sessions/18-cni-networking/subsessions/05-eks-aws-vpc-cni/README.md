# Sub-Session 05: EKS And AWS VPC CNI

This sub-session explains the default Pod networking model on Amazon EKS.

## Main Idea

AWS VPC CNI assigns VPC IP addresses to Pods.

That means a Pod IP is not just an overlay address inside Kubernetes. It is an
address from the VPC subnets attached to the worker Nodes.

Mental model:

```text
EC2 Node
  -> Elastic Network Interface
    -> secondary private IPs or prefixes
      -> assigned to Pods
```

## Components

Common EKS CNI components:

- `aws-node` DaemonSet in `kube-system`.
- `aws-node` Pod running on every Node.
- `ipamd`, the IP address management process.
- ENIs attached to EC2 worker Nodes.
- Warm IP or warm prefix targets.

Inspect:

```bash
kubectl get daemonset aws-node -n kube-system
kubectl get pods -n kube-system -l k8s-app=aws-node -o wide
kubectl describe daemonset aws-node -n kube-system
```

Logs:

```bash
kubectl logs -n kube-system -l k8s-app=aws-node --tail=100
```

## How Pod IP Allocation Works

Simplified flow:

```text
1. aws-node runs on each worker Node.
2. ipamd keeps a warm pool of available Pod IPs or prefixes.
3. When a Pod starts, CNI asks for an IP.
4. ipamd assigns one available VPC IP to the Pod.
5. The Pod receives that IP on its network interface.
6. VPC routing handles traffic to other VPC destinations.
```

The exact behavior depends on configuration, instance type, subnet capacity, and
whether prefix delegation is enabled.

## Why This Is Different From Flannel

Flannel VXLAN:

```text
Pod IP is usually from a cluster overlay CIDR.
Cross-Node packets are encapsulated.
Physical network sees Node IP to Node IP.
```

AWS VPC CNI:

```text
Pod IP is from the VPC subnet.
VPC can route to the Pod IP.
No generic VXLAN overlay is needed for the normal Pod path.
```

## Strengths

- Native AWS networking.
- Pod IPs are routable in the VPC.
- Good integration with AWS load balancing.
- Familiar VPC security and routing model.
- Works naturally with EKS managed add-ons.

## Operational Concerns

Watch these carefully:

- Subnet IP exhaustion.
- Per-instance ENI limits.
- Per-instance IP address limits.
- Prefix delegation settings.
- Security groups for Pods, if enabled.
- Custom networking, if Pods should use different subnets.
- Cross-AZ traffic costs and routing.
- NetworkPolicy support and whether it is enabled in your cluster.

## Useful Checks

Pod IPs and Nodes:

```bash
kubectl get pods -A -o wide
kubectl get nodes -o wide
```

aws-node health:

```bash
kubectl get daemonset aws-node -n kube-system
kubectl get pods -n kube-system -l k8s-app=aws-node
kubectl logs -n kube-system -l k8s-app=aws-node --tail=50
```

Environment configuration:

```bash
kubectl set env daemonset/aws-node -n kube-system --list
```

Use the command above only to inspect. Do not change values during the class
unless the lab explicitly calls for it.

## IP Exhaustion Symptoms

Common symptoms:

```text
failed to assign an IP address to container
failed to setup network for sandbox
Pod stuck in ContainerCreating
Insufficient pods
```

Possible causes:

- Subnet has no available addresses.
- Node instance type cannot attach more ENIs or IPs.
- Warm IP settings are too low or too high for the workload pattern.
- Prefix delegation is disabled where it would help.
- Custom networking configuration is incorrect.

## Prefix Delegation

Prefix delegation lets the CNI assign prefixes to ENIs instead of individual
secondary IP addresses.

This can improve Pod density and IP allocation behavior on supported instance
types and configurations.

Discuss before enabling:

- Instance type support.
- Subnet capacity.
- Existing Pod density needs.
- Compatibility with current EKS add-on version.
- Rollout method.

## NetworkPolicy On EKS

Do not assume NetworkPolicy is enforced just because Kubernetes accepts the
object.

NetworkPolicy enforcement depends on the CNI and configured features. On EKS,
confirm the current networking add-ons and policy support before teaching a
policy lab.

Basic validation:

```bash
kubectl get networkpolicy -A
kubectl get pods -n kube-system
```

Then test actual connectivity. A policy object existing is not proof that
traffic is blocked.

## Review Questions

1. Why does AWS VPC CNI not need a generic overlay for normal Pod networking?
2. What is `aws-node` responsible for?
3. Why can subnet size limit the number of Pods?
4. Why do EC2 instance types matter for Pod density?
5. What is prefix delegation trying to improve?
6. Why must NetworkPolicy behavior be tested instead of assumed?
