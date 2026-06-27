# Sub-Session 08: Troubleshooting, Limitations, And Production Checklist

This sub-session collects the operational side of CNI.

## First Rule Of CNI Debugging

Find the failing layer.

Do not start by changing YAML randomly. First decide whether the problem is:

- Pod scheduling.
- CNI sandbox setup.
- IP allocation.
- Same-Node Pod networking.
- Cross-Node Pod networking.
- Service load balancing.
- DNS.
- NetworkPolicy.
- Cloud security groups, routes, or firewalls.
- MTU.
- Application listener or port mismatch.

## Common Symptoms

Pod stuck before starting:

```text
ContainerCreating
FailedCreatePodSandBox
failed to setup network for sandbox
no IP addresses available
```

Connectivity fails:

```text
DNS lookup fails
Service has no endpoints
Pod IP works but Service IP fails
same-Node works but cross-Node fails
small requests work but large requests hang
NetworkPolicy accepted but traffic still allowed
```

## Kubernetes Checks

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -A --sort-by=.lastTimestamp
```

Service checks:

```bash
kubectl get service -A
kubectl get endpoints -A
kubectl get endpointslices -A
kubectl describe service <service-name> -n <namespace>
```

CNI Pods:

```bash
kubectl get pods -n kube-system -o wide
kubectl get daemonset -n kube-system
```

## Node Checks

Use these only when you have safe access to a Node or an approved debug shell.

```bash
ip addr
ip link
ip route
ip neigh
```

Traditional dataplane:

```bash
iptables -L -n -v
iptables -t nat -L -n -v
conntrack -L
```

eBPF dataplane:

```bash
bpftool prog show
bpftool map show
```

Cilium-specific:

```bash
cilium status
cilium endpoint list
cilium service list
hubble observe --verdict DROPPED
```

Calico-specific:

```bash
calicoctl node status
calicoctl get ippool -o wide
calicoctl get workloadendpoint -A
```

## What CNI Does Not Solve Alone

CNI does not automatically solve:

- Application protocol bugs.
- DNS configuration mistakes.
- Ingress controller behavior.
- TLS or certificate problems.
- Cloud load balancer health checks.
- Cross-account or cross-VPC routing.
- Service mesh policy.
- Every form of encryption.

CNI provides the Pod networking foundation. Other layers still matter.

## Limitations By Approach

Overlay CNIs:

- Encapsulation overhead.
- MTU sensitivity.
- Harder packet captures.

BGP or underlay CNIs:

- Requires routing design.
- Network team coordination.
- Route scale planning.

Cloud CNIs:

- IP exhaustion.
- Instance type limits.
- Provider-specific behavior.
- Subnet planning becomes cluster capacity planning.

iptables-heavy dataplanes:

- Large rule sets at scale.
- Harder troubleshooting.
- Rule update cost during churn.

eBPF dataplanes:

- Kernel and feature compatibility matter.
- Different debugging tools.
- Careful rollout needed.

Multus and SR-IOV:

- More complex scheduling and operations.
- Secondary interfaces may bypass normal policy paths.
- Hardware and driver dependencies.

## Production Checklist

Before choosing or changing a CNI, decide:

- Which Kubernetes versions must be supported?
- Which operating systems and kernels are used?
- What is the Pod CIDR and Service CIDR?
- Is overlay allowed?
- Is BGP allowed?
- How is IPAM handled?
- How is MTU calculated?
- Is NetworkPolicy required?
- Is egress control required?
- Is encryption required?
- Is kube-proxy replacement desired?
- How will the team observe flows?
- How will the team debug drops?
- How are upgrades tested?
- How is rollback handled?
- What happens during Node scale-out?
- What happens during subnet pressure or IP exhaustion?
- What are the cloud provider limits?

## CNI Migration Warning

Replacing a cluster CNI can interrupt all workload networking.

For production:

- Build a separate test cluster.
- Document the current CNI state.
- Validate workloads, Services, DNS, Ingress, and policies.
- Test Node replacement and scaling.
- Test rollback.
- Prefer blue-green cluster migration when possible.

## Troubleshooting Flow

```text
Pod not running?
  -> describe Pod events
  -> inspect CNI DaemonSet and logs
  -> check IP exhaustion

Pod running but cannot resolve DNS?
  -> check CoreDNS
  -> check kube-dns Service
  -> test egress to DNS

DNS works but Service fails?
  -> check Service selector
  -> check EndpointSlices
  -> test backend Pod IP directly

Pod IP works but cross-Node fails?
  -> compare same-Node vs cross-Node
  -> check routes, overlay, security groups, MTU

Traffic unexpectedly allowed or denied?
  -> inspect NetworkPolicy
  -> confirm CNI enforces policy
  -> use CNI-specific flow tools
```

## Review Questions

1. Why should you compare same-Node and cross-Node traffic during debugging?
2. Why can a Service fail even when backend Pods are healthy?
3. What symptoms suggest an MTU problem?
4. Why is cloud subnet capacity part of Kubernetes capacity planning?
5. Why is CNI migration risky?
6. Which tools would you use first for Cilium? For Calico? For AWS VPC CNI?
