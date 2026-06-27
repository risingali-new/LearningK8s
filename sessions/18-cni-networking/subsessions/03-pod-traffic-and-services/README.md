# Sub-Session 03: Pod Traffic And Services

This sub-session follows packets through common Kubernetes networking paths.

## Same-Node Pod-To-Pod Traffic

When two Pods are on the same Node, traffic may stay entirely on that Node.

Bridge-style path:

```text
Pod A eth0
  -> veth pair
    -> Linux bridge
      -> veth pair
        -> Pod B eth0
```

Routing-style path:

```text
Pod A eth0
  -> veth pair
    -> host routing decision
      -> veth pair
        -> Pod B eth0
```

eBPF-style path:

```text
Pod A eth0
  -> eBPF program
    -> map lookup and policy decision
      -> redirect to Pod B
```

## Cross-Node Pod-To-Pod Traffic With Overlay

Overlay path:

```text
Pod A
  -> Node A
    -> encapsulate packet
      -> physical network sees Node A IP to Node B IP
        -> Node B decapsulates
          -> Pod B
```

Common encapsulations:

- VXLAN.
- IP-in-IP.
- Geneve.

Benefits:

- Works even when the physical network does not know Pod CIDRs.
- Easier to deploy in basic networks.

Costs:

- Extra headers.
- MTU planning.
- More complex packet captures.

## Cross-Node Pod-To-Pod Traffic With Underlay Routing

Underlay path:

```text
Pod A
  -> Node A route table
    -> physical network route to Pod B CIDR
      -> Node B
        -> Pod B
```

Common underlay techniques:

- Static routes.
- BGP route advertisements.
- Cloud-native VPC routing.

Benefits:

- No overlay encapsulation.
- Often better performance and easier packet size behavior.

Costs:

- Requires route control.
- Can be harder in locked-down cloud or enterprise networks.

## Service Traffic

A Service selects backend Pods with labels.

Example:

```text
Service backend
  selector:
    app: backend
```

Traffic path with traditional kube-proxy:

```text
Client Pod
  -> ClusterIP
    -> kube-proxy iptables or ipvs rule
      -> backend Pod IP
```

Traffic path with eBPF Service handling:

```text
Client Pod
  -> eBPF service map lookup
    -> backend Pod IP
```

Important point:

```text
CNI gives Pods reachable IPs.
Service handling maps stable virtual IPs to changing Pod IPs.
```

## NodePort And LoadBalancer

NodePort exposes a Service on a port on each Node.

```text
External client
  -> NodeIP:NodePort
    -> Service backend
```

LoadBalancer usually asks the cloud provider to create a cloud load balancer.

```text
Cloud load balancer
  -> NodePort or direct Pod target mode
    -> Service backend
```

On AWS, the exact path depends on the controller and target type:

- Instance target mode sends traffic to Nodes.
- IP target mode can send traffic directly to Pod IPs when supported.

## DNS To Service To Pod

Most apps call Services by DNS name:

```text
backend.cni-lab.svc.cluster.local
```

Flow:

```text
Application
  -> DNS query to CoreDNS
    -> Service ClusterIP returned
      -> packet sent to ClusterIP
        -> Service dataplane selects backend Pod
```

DNS answers the name. The Service dataplane handles the actual traffic.

## Useful Inspection Commands

```bash
kubectl get pods -A -o wide
kubectl get endpoints -A
kubectl get endpointslices -A
kubectl get services -A
```

For a specific Service:

```bash
kubectl describe service <service-name> -n <namespace>
kubectl get endpointslice -n <namespace> -l kubernetes.io/service-name=<service-name>
```

On a Node with safe access:

```bash
ip route
iptables -t nat -L -n -v
```

With Cilium:

```bash
cilium service list
cilium bpf lb list
hubble observe
```

## Traffic Debugging Questions

When traffic fails, ask:

1. Can the source Pod resolve DNS?
2. Can the source Pod reach the Service ClusterIP?
3. Does the Service have Endpoints or EndpointSlices?
4. Can the source Pod reach the backend Pod IP directly?
5. Are source and destination Pods on the same Node or different Nodes?
6. Is NetworkPolicy blocking the traffic?
7. Is cloud security group or network ACL behavior involved?
8. Is MTU involved?

## Review Questions

1. How does same-Node Pod traffic differ from cross-Node Pod traffic?
2. Why do Services need a dataplane implementation?
3. What does kube-proxy do?
4. How can eBPF replace kube-proxy behavior?
5. Why are EndpointSlices useful for debugging Services?
6. Why can direct Pod IP traffic work while Service traffic fails?
