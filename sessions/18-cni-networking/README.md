# Session 18: CNI, Kubernetes Networking, And eBPF

This session explains Kubernetes networking from the Linux building blocks up to
modern eBPF-based CNIs.

The main teaching idea is:

```text
Kubernetes defines the networking model.
CNI defines the plugin contract.
The selected CNI plugin implements Pod networking with Linux networking,
cloud networking, overlays, routing, policy engines, or eBPF.
```

By the end, students should be able to explain what happens when a Pod gets an
IP address, how Pod traffic moves across Nodes, why different CNIs behave
differently, how NetworkPolicy is enforced, and why eBPF changed the Kubernetes
networking dataplane.

## What CNI Is

CNI means Container Network Interface.

CNI is not a network by itself. It is a specification that tells container
runtimes how to call networking plugins.

In Kubernetes, the flow is:

```text
Pod scheduled to Node
  -> kubelet asks the container runtime to create a Pod sandbox
    -> runtime creates a network namespace
      -> runtime calls the configured CNI plugin with ADD
        -> CNI plugin creates interfaces, assigns IPs, routes traffic, and returns a result
```

The CNI plugin may be simple, like a bridge plugin on one host, or advanced,
like Cilium using eBPF programs and maps in the Linux kernel.

## Kubernetes Networking Model

Kubernetes expects these rules:

- Every Pod has its own IP address.
- Pods can reach other Pods without application-level NAT.
- Nodes can reach Pods.
- Containers inside the same Pod share one network namespace.
- Services provide stable virtual addresses in front of changing Pods.

CNI mainly implements Pod networking. Service load balancing is usually handled
by `kube-proxy` with `iptables` or `ipvs`, or by an eBPF dataplane such as
Cilium kube-proxy replacement.

## Core Building Blocks

| Concept | Meaning |
| --- | --- |
| Network namespace | Isolated Linux network stack with its own interfaces, routes, and addresses |
| veth pair | Virtual cable used to connect a Pod namespace to the Node namespace |
| Linux bridge | Layer 2 software switch, often named `cni0` or similar |
| Routing table | Kernel table that decides the next hop for packets |
| Overlay | Encapsulates Pod packets inside Node-to-Node packets, often VXLAN or IP-in-IP |
| Underlay | The real network knows how to route Pod CIDRs directly |
| IPAM | IP address management; decides which Pod gets which IP |
| NetworkPolicy | Kubernetes policy API; enforcement depends on the CNI |
| eBPF | Kernel execution technology used by modern CNIs for fast forwarding, policy, NAT, and observability |

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-networking-foundations`: Linux namespaces, veth pairs, bridges, routes, NAT, MTU, DNS, and Services.
2. `subsessions/02-cni-contract-and-pod-startup`: CNI files, binaries, runtime calls, ADD/DEL/CHECK, and Pod sandbox startup.
3. `subsessions/03-pod-traffic-and-services`: same-Node traffic, cross-Node traffic, overlay, underlay, kube-proxy, and Service paths.
4. `subsessions/04-cni-types-and-configuration`: bridge, Flannel, Calico, Cilium, cloud CNIs, Multus, SR-IOV, and configuration examples.
5. `subsessions/05-eks-aws-vpc-cni`: how the default EKS CNI assigns VPC IPs to Pods and what to watch for.
6. `subsessions/06-network-policy`: hands-on connectivity and NetworkPolicy lab.
7. `subsessions/07-ebpf-and-cilium`: eBPF internals, Cilium, kube-proxy replacement, Hubble, and identity-aware policy.
8. `subsessions/08-troubleshooting-limitations-production`: troubleshooting commands, limitations, production checklist, and review questions.

## Target Mental Model

```text
Kubernetes API
  -> Pod object
    -> kubelet on selected Node
      -> container runtime
        -> Pod sandbox network namespace
          -> CNI ADD
            -> IPAM allocates an address
            -> dataplane connects the Pod
            -> policy engine programs allow/deny rules
            -> runtime starts containers inside the namespace
```

## Typical Files On A Node

CNI binaries usually live here:

```bash
/opt/cni/bin/
```

CNI configuration usually lives here:

```bash
/etc/cni/net.d/
```

On managed Kubernetes services, these paths still often exist on worker Nodes,
but the cloud provider may manage the CNI DaemonSet, config, and lifecycle.

## Full Lab Apply Order

The only runnable manifests in this session are the safe application-level
connectivity and NetworkPolicy lab.

From `sessions/18-cni-networking`:

```bash
kubectl apply -f subsessions/06-network-policy/01-namespace.yml
kubectl apply -f subsessions/06-network-policy/02-connectivity-demo.yml
```

Then test baseline connectivity before applying policies:

```bash
kubectl get pods -n cni-lab -o wide
kubectl exec -n cni-lab deploy/frontend -- wget -qO- http://backend.cni-lab.svc.cluster.local:8080
```

Apply a default deny ingress policy:

```bash
kubectl apply -f subsessions/06-network-policy/03-default-deny-ingress.yml
```

Then allow only frontend-to-backend traffic:

```bash
kubectl apply -f subsessions/06-network-policy/04-allow-frontend-to-backend.yml
```

NetworkPolicy enforcement requires a policy-capable CNI. Plain Flannel does not
enforce Kubernetes NetworkPolicy by itself.

## Optional CNI Implementation Labs

Changing a cluster CNI is a platform operation. Do not replace the CNI on a
shared or production cluster during class.

Use a disposable cluster for install experiments:

- Flannel: simple overlay connectivity, commonly VXLAN.
- Calico: policy, BGP routing, IP-in-IP, VXLAN, or eBPF dataplane.
- Cilium: eBPF dataplane, kube-proxy replacement, Hubble, and advanced policy.
- Multus: multiple Pod interfaces and secondary networks.

Configuration examples are included under:

```text
examples/
```

Treat them as study material and starting points, not blind production defaults.

## Cleanup

From `sessions/18-cni-networking`:

```bash
kubectl delete -f subsessions/06-network-policy/04-allow-frontend-to-backend.yml --ignore-not-found
kubectl delete -f subsessions/06-network-policy/03-default-deny-ingress.yml --ignore-not-found
kubectl delete -f subsessions/06-network-policy/02-connectivity-demo.yml --ignore-not-found
kubectl delete -f subsessions/06-network-policy/01-namespace.yml --ignore-not-found
```

## Review Questions

1. What problem does the CNI specification solve?
2. Why does each Pod get its own network namespace?
3. What is a veth pair, and why is it useful?
4. What is the difference between overlay and underlay networking?
5. Why does MTU become important with VXLAN or IP-in-IP?
6. What is IPAM responsible for?
7. Why does Kubernetes NetworkPolicy require CNI support?
8. How does AWS VPC CNI differ from Flannel?
9. Why might a team choose Calico BGP instead of VXLAN?
10. Why can eBPF replace large parts of `iptables` and `kube-proxy`?
11. What does Cilium identity-based policy solve that IP-only policy struggles with?
12. What are the operational risks of replacing a cluster CNI?

## References

- Kubernetes cluster networking: `https://kubernetes.io/docs/concepts/cluster-administration/networking/`
- Kubernetes NetworkPolicy: `https://kubernetes.io/docs/concepts/services-networking/network-policies/`
- CNI specification: `https://github.com/containernetworking/cni`
- CNI plugins: `https://github.com/containernetworking/plugins`
- AWS VPC CNI: `https://github.com/aws/amazon-vpc-cni-k8s`
- Calico documentation: `https://docs.tigera.io/calico/latest/about/`
- Cilium documentation: `https://docs.cilium.io/`
- Linux eBPF documentation: `https://docs.kernel.org/bpf/`
