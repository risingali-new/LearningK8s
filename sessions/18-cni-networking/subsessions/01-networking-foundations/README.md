# Sub-Session 01: Networking Foundations

This sub-session builds the Linux networking foundation needed to understand
CNI.

## Why Linux Networking Matters

Kubernetes networking is not magic. A CNI plugin mostly programs normal Linux
networking objects:

- Network namespaces.
- Interfaces.
- veth pairs.
- Bridges.
- Routes.
- Neighbor tables.
- `iptables`, `nftables`, or eBPF programs.
- Encapsulation devices such as VXLAN.

When a Pod cannot talk to another Pod, the answer is usually visible somewhere
in those objects.

## Network Namespace

A network namespace is an isolated network stack.

Each Pod gets a network namespace with its own:

- Interfaces.
- IP addresses.
- Routes.
- ARP or neighbor table.
- Local ports.

Containers inside one Pod share this namespace. That is why two containers in
the same Pod can talk to each other over `localhost`.

Mental model:

```text
Pod network namespace
  eth0
  10.x.x.x
  default route
  local ports
```

## veth Pair

A veth pair is a virtual cable with two ends.

Common Pod shape:

```text
Pod namespace                    Node namespace
-------------                    --------------
eth0        <---- veth pair ---> vethabc123
```

Traffic from the Pod leaves through `eth0`, crosses the veth pair, and appears
on the host side as a normal Linux interface.

## Bridge

A Linux bridge is a software switch.

Bridge-based CNIs connect many Pod veth interfaces to one bridge:

```text
Pod A eth0 -> vethA -> cni0
Pod B eth0 -> vethB -> cni0
Pod C eth0 -> vethC -> cni0
```

The bridge learns MAC addresses and forwards frames like a Layer 2 switch.

## Routing

Linux routing decides where packets go after the kernel receives them.

Important commands:

```bash
ip addr
ip link
ip route
ip neigh
```

Example route meaning:

```text
10.244.2.0/24 via 192.168.10.22 dev eth0
```

Traffic for Pods in `10.244.2.0/24` should be sent to Node
`192.168.10.22` through `eth0`.

## NAT And Masquerade

NAT changes packet source or destination addresses.

Common Kubernetes uses:

- Pod egress to the internet may be source NATed to the Node IP.
- Service traffic may be destination NATed to a backend Pod.
- NodePort traffic may be redirected to a Service backend.

Traditional clusters often use `iptables` rules for this.

Useful checks:

```bash
iptables -t nat -L -n -v
iptables -L -n -v
```

Some newer clusters use `nftables` or eBPF instead of large `iptables` rule
sets.

## Overlay Networking

Overlay networking encapsulates a Pod packet inside a Node packet.

Example with VXLAN:

```text
Outer packet:
  source: Node A IP
  dest:   Node B IP

Inner packet:
  source: Pod A IP
  dest:   Pod B IP
```

Overlay is useful when the physical network does not know Pod CIDRs.

Tradeoffs:

- Easier to deploy across many environments.
- Adds encapsulation overhead.
- Reduces effective MTU.
- Can make packet captures harder to read.

## Underlay Networking

Underlay networking means the real network knows how to route Pod addresses.

Example:

```text
Data center router knows:
  10.10.1.0/24 is behind Node A
  10.10.2.0/24 is behind Node B
```

This avoids overlay encapsulation, but requires routing integration. Calico with
BGP is a common example.

## MTU

MTU is the largest packet size that can pass through an interface without
fragmentation.

Overlays add headers. If the physical network MTU is `1500`, VXLAN overhead can
make an original `1500` byte Pod packet too large.

Symptoms of MTU problems:

- Small requests work, large requests hang.
- TLS connections fail mysteriously.
- Some cross-Node traffic fails but same-Node traffic works.

Useful checks:

```bash
ip link
ping -M do -s 1472 <destination-ip>
```

The exact packet size depends on the network and encapsulation overhead.

## DNS In Kubernetes

DNS is not CNI, but students often debug both together.

Pod DNS queries usually go to CoreDNS:

```text
Pod
  -> kube-dns Service IP
    -> CoreDNS Pod
      -> cluster DNS answer or upstream resolver
```

Useful checks:

```bash
kubectl get service kube-dns -n kube-system
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide
```

## Service Networking

A Service is a stable virtual frontend for changing Pods.

Typical `ClusterIP` path with `kube-proxy`:

```text
Client Pod
  -> Service ClusterIP
    -> kube-proxy rule
      -> selected backend Pod IP
```

With eBPF Service handling:

```text
Client Pod
  -> eBPF service lookup
    -> selected backend Pod IP
```

CNI and Service networking are closely related, but they are not the same
layer.

## Commands To Run On A Cluster

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get services -A
```

If you have safe Node shell access:

```bash
ip addr
ip link
ip route
ip neigh
```

On managed clusters, use provider-supported debug methods before logging into
Nodes directly.

## Review Questions

1. Why does Kubernetes use network namespaces for Pods?
2. What does a veth pair connect?
3. Why might a CNI use a Linux bridge?
4. What is the difference between routing and bridging?
5. Why can overlay networking cause MTU issues?
6. Why is DNS not the same thing as CNI?
