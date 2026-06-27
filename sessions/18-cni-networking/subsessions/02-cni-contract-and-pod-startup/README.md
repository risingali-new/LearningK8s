# Sub-Session 02: CNI Contract And Pod Startup

This sub-session explains the CNI specification and how Kubernetes uses it when
a Pod starts.

## The CNI Contract

CNI defines a small contract between a container runtime and a network plugin.

The runtime provides:

- Container or sandbox ID.
- Network namespace path.
- Interface name to create inside the namespace, usually `eth0`.
- CNI configuration JSON.
- Command such as `ADD`, `DEL`, `CHECK`, or `VERSION`.

The plugin returns:

- Assigned interface details.
- IP address.
- Routes.
- DNS data, if configured.
- Success or error.

## Who Calls CNI

In Kubernetes, kubelet does not usually call the CNI binary directly.

Typical flow:

```text
kubelet
  -> CRI request
    -> containerd or CRI-O
      -> CNI plugin executable
```

The runtime creates the Pod sandbox and network namespace, then calls CNI to
connect that namespace to the cluster network.

## Common CNI Commands

| Command | When it happens | Purpose |
| --- | --- | --- |
| `ADD` | Pod sandbox creation | Create networking for the Pod |
| `DEL` | Pod sandbox deletion | Remove networking and release IPs |
| `CHECK` | Runtime validation | Confirm the network still matches expectations |
| `VERSION` | Runtime/plugin negotiation | Report supported CNI spec versions |

## Pod Startup Sequence

```text
1. User creates Pod.
2. Scheduler assigns the Pod to a Node.
3. kubelet sees the assigned Pod.
4. kubelet asks the container runtime to create a sandbox.
5. Runtime creates a network namespace for the sandbox.
6. Runtime reads CNI configuration from /etc/cni/net.d/.
7. Runtime calls the CNI plugin binary from /opt/cni/bin/.
8. CNI plugin calls IPAM or its own IP allocator.
9. CNI plugin creates interfaces, routes, and dataplane state.
10. Runtime starts the application containers inside the ready Pod namespace.
```

If the CNI step fails, the Pod often stays in `ContainerCreating`.

## Important Node Paths

CNI config:

```bash
/etc/cni/net.d/
```

CNI binaries:

```bash
/opt/cni/bin/
```

Runtime CNI state is often under directories such as:

```bash
/var/lib/cni/
/var/run/netns/
/run/netns/
```

Exact paths vary by OS, runtime, distribution, and managed service.

## Example CNI Config

A small bridge-style config may look like:

```json
{
  "cniVersion": "1.0.0",
  "name": "training-bridge",
  "type": "bridge",
  "bridge": "cni0",
  "isGateway": true,
  "ipMasq": true,
  "ipam": {
    "type": "host-local",
    "ranges": [
      [
        {
          "subnet": "10.244.1.0/24"
        }
      ]
    ],
    "routes": [
      {
        "dst": "0.0.0.0/0"
      }
    ]
  }
}
```

This is a CNI configuration example, not a complete Kubernetes production
network.

## IPAM

IPAM means IP address management.

It answers:

- Which Pod IP should this sandbox receive?
- Is the address already in use?
- What routes should be returned?
- How is the IP released when the Pod is deleted?

Common IPAM approaches:

- `host-local`: stores allocations locally on each Node.
- DHCP: receives IPs from a DHCP server.
- Cloud IPAM: allocates VPC/VNet addresses from the cloud provider.
- Calico IPAM: allocates from Calico IP pools.
- Cilium IPAM: supports Kubernetes, cluster-pool, cloud, and operator-managed modes.
- Whereabouts: commonly used with Multus for cluster-wide secondary network IPAM.

## CNI Plugin Chaining

A CNI configuration can be a plugin list.

Example concept:

```text
main plugin creates connectivity
  -> portmap plugin adds hostPort support
    -> bandwidth plugin applies traffic shaping
      -> tuning plugin sets sysctls or interface attributes
```

This is why many Kubernetes CNI config files use `.conflist` instead of a
single `.conf`.

## Failure Examples

Common Pod events:

```text
FailedCreatePodSandBox
failed to setup network for sandbox
networkPlugin cni failed to set up pod
no IP addresses available
failed to find plugin "bridge" in path
CNI config uninitialized
```

First checks:

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get pods -n kube-system -o wide
kubectl logs -n kube-system -l k8s-app=aws-node
```

The exact CNI label differs by plugin. For example, AWS VPC CNI commonly uses
the `aws-node` DaemonSet, while Cilium uses `cilium` Pods.

## Review Questions

1. Does kubelet usually call CNI directly?
2. What does CNI `ADD` do?
3. Why does a Pod stay in `ContainerCreating` when CNI fails?
4. What is the difference between CNI config and CNI binaries?
5. Why does IPAM matter?
6. Why might a CNI use plugin chaining?
