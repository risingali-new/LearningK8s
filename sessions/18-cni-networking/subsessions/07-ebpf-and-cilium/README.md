# Sub-Session 07: eBPF And Cilium

This sub-session explains how eBPF changes Kubernetes networking and why Cilium
is important in modern clusters.

## What eBPF Is

eBPF lets small verified programs run inside the Linux kernel at defined hook
points.

Networking hooks include:

- XDP, very early in packet processing.
- TC ingress and egress.
- Socket hooks.
- cgroup hooks.

eBPF programs use maps to store and read state.

Examples of maps:

- Service frontend to backend mappings.
- Connection tracking state.
- NAT state.
- Endpoint identities.
- Policy decisions.

## Traditional Dataplane

Traditional Kubernetes networking often relies on:

```text
Linux bridge
  -> routing
    -> iptables
      -> conntrack
        -> destination
```

This works, but large clusters can produce very large `iptables` rule sets.
Debugging can also be difficult because decisions are spread across many chains
and tables.

## eBPF Dataplane

With eBPF:

```text
Packet arrives
  -> eBPF program runs at a hook
    -> map lookup
      -> policy, NAT, service, or forwarding decision
        -> pass, drop, redirect, or rewrite
```

Benefits:

- Fewer long `iptables` chains.
- Fast map lookups.
- Better per-flow observability.
- Easier service load balancing at scale.
- Richer security context.

## What Cilium Uses eBPF For

Cilium can use eBPF for:

- Pod connectivity.
- NetworkPolicy enforcement.
- Service load balancing.
- kube-proxy replacement.
- NAT.
- Connection tracking.
- Host firewalling.
- Transparent encryption integration.
- Flow observability with Hubble.

## Identity-Aware Policy

IP addresses are temporary in Kubernetes.

Traditional IP-based thinking:

```text
Allow 10.20.1.15 to reach 10.20.2.44
```

Cilium identity thinking:

```text
Allow Pods with app=frontend to reach Pods with app=backend
```

Cilium maps workload labels to security identities, then enforces policy using
those identities.

This is useful because Pods are recreated often and IPs change.

## kube-proxy Replacement

kube-proxy normally programs Service load balancing with `iptables` or `ipvs`.

Cilium can replace kube-proxy with eBPF Service handling.

Traditional:

```text
Service ClusterIP
  -> kube-proxy rule
    -> backend Pod
```

Cilium:

```text
Service ClusterIP
  -> eBPF load-balancer map
    -> backend Pod
```

This can improve performance and visibility, especially in large clusters.

## Hubble

Hubble is Cilium's observability layer.

It can show:

- Source and destination identities.
- Allowed or denied flows.
- DNS queries.
- HTTP information, when L7 visibility is enabled.
- Service and Pod traffic paths.

Useful commands on a Cilium cluster:

```bash
cilium status
cilium connectivity test
hubble observe
hubble observe --namespace cni-lab
```

## Optional Cilium Install Shape

Use a disposable cluster for this lab.

General install shape with the Cilium CLI:

```bash
cilium install
cilium status --wait
cilium connectivity test
```

For kube-proxy replacement, the cluster must be prepared correctly. Do not turn
this on casually in an existing cluster.

Study example:

```text
examples/cilium-values-kubeproxy-replacement.yml
```

## eBPF Is Not Magic

eBPF has limits and requirements:

- Kernel version matters.
- CNI feature flags matter.
- Some cloud environments have special constraints.
- Tooling is different from classic `iptables` debugging.
- Incorrect rollout can break cluster networking.
- Teams need observability and operational practice.

## Useful Commands

Cilium:

```bash
cilium status
cilium config view
cilium service list
cilium endpoint list
cilium policy get
```

Hubble:

```bash
hubble status
hubble observe
hubble observe --verdict DROPPED
```

Linux eBPF inspection, if tools are installed:

```bash
bpftool prog show
bpftool map show
```

## Review Questions

1. Why can eBPF reduce dependence on large `iptables` rule sets?
2. What is an eBPF map?
3. How does Cilium use workload identity?
4. What does kube-proxy replacement mean?
5. What kind of visibility does Hubble provide?
6. Why should eBPF CNI rollout be planned carefully?
