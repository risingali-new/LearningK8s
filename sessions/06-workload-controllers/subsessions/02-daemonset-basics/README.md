# Sub-Session 02: DaemonSet Basics

This sub-session creates a small `node-reporter` DaemonSet.

The container prints its Pod name, Namespace, and Node name every 30 seconds. This makes it easy to see that Kubernetes runs one DaemonSet Pod per matching Node.

## Why DaemonSet Is Used

A DaemonSet is used when a workload should run on Nodes, not just as a pool of app replicas.

Common examples:

- Log collector on every Node.
- Metrics agent on every Node.
- Network plugin agent on every Node.
- Storage plugin agent on every Node.

This lab uses a simple BusyBox container instead of a real logging or monitoring agent so the behavior is easy to observe.

## Apply

From `sessions/06-workload-controllers`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
kubectl apply -f subsessions/02-daemonset-basics/
```

## Check

```bash
kubectl get daemonset node-reporter -n daemonset-lab
kubectl get pods -n daemonset-lab -l app=node-reporter -o wide
```

Compare the desired/current/ready count with the number of eligible Nodes:

```bash
kubectl get nodes
kubectl get daemonset node-reporter -n daemonset-lab
```

## Inspect Logs

```bash
kubectl logs -n daemonset-lab -l app=node-reporter --tail=20 --prefix
```

Each Pod should report a different `node=...` value when the cluster has multiple Nodes.

## Self-Healing Test

Delete the DaemonSet Pods:

```bash
kubectl delete pod -n daemonset-lab -l app=node-reporter
kubectl get pods -n daemonset-lab -l app=node-reporter -o wide -w
```

The DaemonSet recreates the missing Pods because each matching Node still needs one.

## Important Detail

DaemonSets do not use `replicas`.

This is valid for a Deployment:

```bash
kubectl scale deployment some-app --replicas=5
```

That is not how DaemonSets are scaled. A DaemonSet gets more Pods when more matching Nodes exist, or when its node selection rules match more Nodes.

## Cleanup

```bash
kubectl delete -f subsessions/02-daemonset-basics/ --ignore-not-found
```

## Review Questions

1. Why does this object create one Pod per Node?
2. What happens if you delete a DaemonSet Pod?
3. Why does a DaemonSet not have a `replicas` field?
4. How could you limit a DaemonSet to only selected Nodes?
