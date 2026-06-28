# Sub-Session 02: Node Selector And Node Affinity

This sub-session compares simple exact-match placement with more expressive
affinity rules.

## Concepts

`nodeSelector` is the simplest scheduler constraint:

```text
Only run this Pod on Nodes with this exact label.
```

Node affinity is more expressive:

```text
requiredDuringSchedulingIgnoredDuringExecution
  -> hard rule

preferredDuringSchedulingIgnoredDuringExecution
  -> soft preference
```

The `IgnoredDuringExecution` part means the Pod is not evicted if the Node label
changes after the Pod is already running.

## Apply

Label one node first:

```bash
export SCHED_NODE=<node-name>
kubectl label node "$SCHED_NODE" training.k8s.io/node-role=scheduling-lab --overwrite
```

From `sessions/10-advanced-scheduling`:

```bash
kubectl apply -f subsessions/02-node-selector-and-node-affinity/01-node-selector-deployment.yml
kubectl apply -f subsessions/02-node-selector-and-node-affinity/02-required-node-affinity-deployment.yml
kubectl apply -f subsessions/02-node-selector-and-node-affinity/03-preferred-node-affinity-deployment.yml
```

## Check

```bash
kubectl get pods -n scheduling-lab -o wide
kubectl describe pod -n scheduling-lab -l app=node-selector-demo
kubectl describe pod -n scheduling-lab -l app=required-affinity-demo
```

Both the `nodeSelector` and required affinity examples should land on the labeled
node. The preferred affinity example can still run elsewhere if needed.

## Break It On Purpose

Remove the node label:

```bash
kubectl label node "$SCHED_NODE" training.k8s.io/node-role-
kubectl rollout restart deployment/node-selector-demo -n scheduling-lab
```

Now inspect the Pending Pod:

```bash
kubectl get pods -n scheduling-lab -o wide
kubectl describe pod -n scheduling-lab -l app=node-selector-demo
```

Restore the label before continuing:

```bash
kubectl label node "$SCHED_NODE" training.k8s.io/node-role=scheduling-lab --overwrite
```

## Cleanup

```bash
kubectl delete -f subsessions/02-node-selector-and-node-affinity/ --ignore-not-found
```
