# Sub-Session 04: CNI Types And Configuration

This sub-session compares common CNI implementations and the configuration
choices behind them.

## CNI Selection Categories

| Category | Examples | Main idea |
| --- | --- | --- |
| Simple bridge | CNI bridge plugin | Connect local containers through a Linux bridge |
| Simple overlay | Flannel | Provide Pod-to-Pod connectivity with minimal policy features |
| Policy and routing | Calico | NetworkPolicy plus overlay, BGP, or eBPF dataplane options |
| eBPF-first | Cilium | eBPF dataplane, identity-aware policy, observability, kube-proxy replacement |
| Cloud-native | AWS VPC CNI, Azure CNI, GKE Dataplane | Integrate Pod IPs with cloud VPC/VNet networking |
| Multi-network | Multus | Attach multiple interfaces to Pods |
| High-performance data plane | SR-IOV, DPDK with Multus | Direct or near-direct NIC access for special workloads |

## Bridge CNI

The bridge plugin is good for learning because it exposes the basic Linux
objects clearly.

It usually creates:

- A Linux bridge.
- One veth pair per container or Pod sandbox.
- A default route inside the namespace.
- Optional masquerade for outbound traffic.

It is not a complete multi-Node Kubernetes networking solution by itself.

Study example:

```text
examples/bridge-cni-conflist.json
```

## Flannel

Flannel focuses on simple Pod connectivity.

Common mode:

```text
VXLAN overlay
```

Strengths:

- Simple to understand.
- Good for basic labs.
- Low operational surface.

Limitations:

- Does not enforce Kubernetes NetworkPolicy by itself.
- Less feature-rich than Calico or Cilium.
- Overlay MTU must be planned.

## Calico

Calico is a production-grade CNI and policy system.

Common modes:

- BGP with no overlay.
- IP-in-IP overlay.
- VXLAN overlay.
- eBPF dataplane.

Strengths:

- Kubernetes NetworkPolicy.
- Calico NetworkPolicy and GlobalNetworkPolicy.
- Strong routing options.
- Good fit for bare metal and advanced routing environments.

Be careful with:

- BGP design and route advertisement.
- IP pool planning.
- Overlay and MTU settings.
- Host endpoint policy if protecting Nodes.

Study examples:

```text
examples/calico-ippool-vxlan.yml
examples/calico-ippool-bgp-no-encap.yml
```

## Cilium

Cilium is an eBPF-based CNI.

It can provide:

- Pod networking.
- Kubernetes NetworkPolicy.
- CiliumNetworkPolicy.
- eBPF Service load balancing.
- kube-proxy replacement.
- Hubble flow observability.
- L7 policy through Envoy integration.
- Transparent encryption.
- Cluster mesh.

Strengths:

- Modern dataplane.
- Excellent observability.
- Scales better than large `iptables` rule sets in many environments.
- Identity-aware policy instead of only IP-based policy.

Be careful with:

- Kernel requirements.
- Feature flags and operating mode.
- kube-proxy replacement compatibility.
- Rollout planning on existing clusters.

Study example:

```text
examples/cilium-values-kubeproxy-replacement.yml
```

## Cloud CNIs

Cloud CNIs integrate Pod networking with the provider network.

AWS VPC CNI:

- Assigns VPC IPs to Pods.
- Uses ENIs and secondary IPs or prefix delegation.
- Makes Pod IPs routable inside the VPC.

Azure CNI and GKE-native approaches have similar goals, but details differ by
provider.

Strengths:

- Cloud-native routing.
- No generic overlay in the common path.
- Better integration with load balancers and cloud security features.

Be careful with:

- IP exhaustion.
- Per-instance network interface limits.
- Provider-specific behavior.
- Cluster scaling and subnet sizing.

## Multus

Multus is a meta-plugin. It lets a Pod attach to more than one network.

Example use cases:

- Telecom workloads.
- Network appliances.
- Storage networks.
- Separate management and data interfaces.
- SR-IOV interfaces.

Typical Pod shape:

```text
eth0: default Kubernetes network
net1: secondary network from Multus
```

Study example:

```text
examples/multus-network-attachment-definition.yml
```

## SR-IOV

SR-IOV allows a physical NIC to expose virtual functions that can be assigned
directly to workloads.

It is useful for:

- High throughput.
- Low latency.
- Network function virtualization.

Tradeoffs:

- More hardware-specific.
- Less flexible than normal Pod networking.
- Scheduling and resource management become important.
- NetworkPolicy may not apply in the same way on the secondary interface.

## Choosing A CNI

For a beginner lab:

```text
Flannel
```

For policy-heavy production:

```text
Calico or Cilium
```

For AWS-native EKS networking:

```text
AWS VPC CNI
```

For modern eBPF and observability:

```text
Cilium
```

For multiple Pod interfaces:

```text
Multus
```

For high-performance packet processing:

```text
SR-IOV, DPDK, or specialized CNI combinations
```

## Configuration Topics To Discuss

When configuring any CNI, discuss:

- Pod CIDR and service CIDR.
- IPAM mode.
- Encapsulation mode.
- MTU.
- NetworkPolicy support.
- kube-proxy mode or replacement.
- Encryption.
- Observability.
- Cloud integration.
- Upgrade path.
- Day-two troubleshooting.

## Review Questions

1. Why is bridge CNI useful for learning but not enough for most Kubernetes clusters?
2. What does Flannel intentionally keep simple?
3. Why might Calico use BGP?
4. Why might Cilium replace kube-proxy?
5. What problem does Multus solve?
6. Why can cloud CNIs run into IP exhaustion?
