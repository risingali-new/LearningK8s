# Sub-Session 01: Prerequisites And Namespace

This sub-session creates a dedicated Namespace for the DaemonSet labs.

## Prerequisites

You need:

- A working Kubernetes cluster.
- `kubectl` configured.
- At least one schedulable worker Node.

Check the cluster:

```bash
kubectl version
kubectl get nodes -o wide
```

## Apply

From `sessions/06-workload-controllers`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
```

## Check

```bash
kubectl get namespace daemonset-lab
kubectl get all -n daemonset-lab
```

At this point, the Namespace should exist but no workload Pods should be running yet.

## Cleanup

Run this only after the later sub-sessions are deleted:

```bash
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
```
