# Sub-Session 04: Taints And Tolerations

This sub-session shows how Nodes can repel Pods unless those Pods explicitly
tolerate the taint.

## Concepts

A taint is placed on a Node:

```text
training.k8s.io/dedicated=scheduling:NoSchedule
```

A toleration is placed on a Pod:

```text
This Pod is allowed to run on Nodes with that taint.
```

A toleration does not force the Pod onto the tainted Node. It only allows the Pod
to be scheduled there. Combine tolerations with node affinity or `nodeSelector`
when you want both permission and placement.

## Taint One Worker Node

Pick a non-critical worker node:

```bash
export SCHED_NODE=<node-name>
kubectl label node "$SCHED_NODE" training.k8s.io/node-role=scheduling-lab --overwrite
kubectl taint node "$SCHED_NODE" training.k8s.io/dedicated=scheduling:NoSchedule --overwrite
```

Check the taint:

```bash
kubectl describe node "$SCHED_NODE" | grep -i taints
```

## Apply The Pod Without A Toleration

From `sessions/10-advanced-scheduling`:

```bash
kubectl apply -f subsessions/04-taints-and-tolerations/01-no-toleration-pod.yml
kubectl get pod no-toleration-demo -n scheduling-lab -o wide
kubectl describe pod no-toleration-demo -n scheduling-lab
```

The Pod selects the tainted node by label, but it has no toleration. It should
stay Pending.

## Apply The Pod With A Toleration

```bash
kubectl apply -f subsessions/04-taints-and-tolerations/02-toleration-pod.yml
kubectl get pod toleration-demo -n scheduling-lab -o wide
```

This Pod has both:

- a `nodeSelector` for the labeled node;
- a toleration for the taint.

## Cleanup

```bash
kubectl delete -f subsessions/04-taints-and-tolerations/ --ignore-not-found
kubectl taint node "$SCHED_NODE" training.k8s.io/dedicated=scheduling:NoSchedule-
```
