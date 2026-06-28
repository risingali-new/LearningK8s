# Sub-Session 01: Prerequisites And Namespace

This sub-session creates a separate Namespace for scheduling labs.

## Create The Namespace

From `sessions/10-advanced-scheduling`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
```

## Inspect Nodes

```bash
kubectl get nodes -o wide
kubectl get nodes --show-labels
```

Most clusters already have useful labels:

- `kubernetes.io/hostname`
- `topology.kubernetes.io/zone`
- `node.kubernetes.io/instance-type`

For the node selector and taint labs, label one worker node:

```bash
export SCHED_NODE=<node-name>
kubectl label node "$SCHED_NODE" training.k8s.io/node-role=scheduling-lab --overwrite
```

Check the label:

```bash
kubectl get node "$SCHED_NODE" --show-labels
```

## Cleanup

Only clean up after all scheduling labs are finished:

```bash
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
kubectl label node "$SCHED_NODE" training.k8s.io/node-role-
```
