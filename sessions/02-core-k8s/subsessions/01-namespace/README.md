# Sub-Session 01: Namespace

This sub-session starts the Kubernetes implementation of the app by creating a dedicated namespace.

## Why Namespace Is Used

A Namespace groups related Kubernetes resources. Without it, everything is created in `default`, which becomes difficult to manage when many apps, students, or sessions share the same cluster.

For this app, the namespace is:

```text
app-core
```

## How Kubernetes Uses It

Namespaced objects such as Pods, Deployments, Services, ConfigMaps, and Secrets are created inside a namespace.

The namespace gives us a clean boundary for:

- Listing app resources.
- Deleting the app resources.
- Avoiding name collisions.
- Teaching one application in isolation.

## Manifest

```text
01-namespace.yml
```

It creates:

```yaml
kind: Namespace
metadata:
  name: app-core
```

## Apply

From `sessions/02-core-k8s`:

```bash
kubectl apply -f subsessions/01-namespace/
```

## Check

```bash
kubectl get namespaces
kubectl get all -n app-core
```

At this point, the namespace exists but no application workloads are running yet.

