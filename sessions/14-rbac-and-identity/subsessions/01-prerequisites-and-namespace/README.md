# Sub-Session 01: Prerequisites And Namespace

This sub-session creates a dedicated Namespace for RBAC practice.

## Why Use A Separate Namespace

RBAC examples are easier to understand when they are isolated.

The lab Namespace lets students safely answer questions like:

- Can this identity read Pods here?
- Can this identity read Pods somewhere else?
- Does this binding grant namespace-level or cluster-level access?

## Prerequisites

You need:

- A working Kubernetes cluster.
- `kubectl` configured.
- Permission to create Namespaces.
- Permission to create RBAC objects in later sub-sessions.

Check the cluster:

```bash
kubectl version
kubectl get nodes
kubectl auth can-i create namespaces
```

## Apply

From `sessions/14-rbac-and-identity`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
```

## Check

```bash
kubectl get namespace rbac-lab
kubectl get all -n rbac-lab
```

At this point, the Namespace should exist but no workloads or RBAC bindings
should be present.

## Cleanup

Run this only after the later sub-sessions are deleted:

```bash
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
```
