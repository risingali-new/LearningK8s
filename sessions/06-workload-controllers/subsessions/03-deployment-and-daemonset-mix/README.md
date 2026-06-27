# Sub-Session 03: Deployment And DaemonSet Mix

This sub-session runs a normal web Deployment beside a node-agent DaemonSet.

The lab creates:

- `mix-web` Deployment with four nginx Pods.
- `mix-web` ClusterIP Service.
- `mix-node-agent` DaemonSet with one small agent Pod per matching Node.

## How The Mix Works

The Deployment is application-level:

```text
mix-web Deployment
  -> four nginx Pods
  -> scheduler places them wherever there is capacity
```

The DaemonSet is node-level:

```text
mix-node-agent DaemonSet
  -> one agent Pod on each matching Node
```

They run in the same Namespace but use different labels and selectors.

## Apply

From `sessions/06-workload-controllers`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
kubectl apply -f subsessions/03-deployment-and-daemonset-mix/
```

## Check The Controllers

```bash
kubectl get deployment mix-web -n daemonset-lab
kubectl get service mix-web -n daemonset-lab
kubectl get daemonset mix-node-agent -n daemonset-lab
```

## Check Pod Placement

```bash
kubectl get pods -n daemonset-lab -o wide
```

Expected result on a two-node cluster:

```text
mix-web:        4 Pods total, placement can vary
mix-node-agent: 2 Pods total, one per Node
```

The Deployment Pods may not be evenly spread unless scheduling constraints request that. The DaemonSet Pods should map to Nodes.

## Scale The Deployment

```bash
kubectl scale deployment mix-web -n daemonset-lab --replicas=6
kubectl get pods -n daemonset-lab -l app=mix-web -o wide
```

Only the Deployment Pod count changes.

Check the DaemonSet again:

```bash
kubectl get daemonset mix-node-agent -n daemonset-lab
kubectl get pods -n daemonset-lab -l app=mix-node-agent -o wide
```

The DaemonSet Pod count stays tied to the number of matching Nodes.

## Test Service Routing

Run a temporary curl Pod:

```bash
kubectl run curl-test --rm -i --restart=Never --image=curlimages/curl:8.10.1 -n daemonset-lab -- curl -s http://mix-web
```

The Service sends traffic to the `mix-web` Deployment Pods. It does not send traffic to the DaemonSet Pods because their labels do not match the Service selector.

## Selector Check

Deployment selector:

```yaml
app: mix-web
workload: deployment
```

DaemonSet selector:

```yaml
app: mix-node-agent
workload: daemonset
```

Service selector:

```yaml
app: mix-web
workload: deployment
```

This is the safe pattern when running both in the same Namespace.

## Cleanup

```bash
kubectl delete -f subsessions/03-deployment-and-daemonset-mix/ --ignore-not-found
```

## Review Questions

1. Which object controls the `mix-web` Pod count?
2. Which object controls the `mix-node-agent` Pod count?
3. Why does scaling the Deployment not change the DaemonSet?
4. Why does the Service route only to the Deployment Pods?
5. What could go wrong if both controllers used the same selector?
