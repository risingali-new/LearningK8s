# Session 01: Kubernetes Architecture

This session explains how Kubernetes works internally before students create
application objects.

## Sub-Session Order

1. `01-control-plane-overview`: API server, etcd, scheduler, controller manager.
2. `02-worker-node-overview`: kubelet, container runtime, kube-proxy, CNI.
3. `03-reconciliation-loop`: desired state, observed state, controllers.
4. `04-pod-scheduling-flow`: from YAML to a running Pod.
5. `05-api-resources-and-objects`: Group, Version, Kind, Resource, Namespace.
6. `06-managed-cluster-view`: what EKS manages and what worker nodes run.

## Target Mental Model

```text
kubectl
  -> API server
    -> etcd stores desired state
    -> scheduler picks Nodes for Pods
    -> controllers create/update child objects
      -> kubelet starts containers through the runtime
```

## Useful Commands

```bash
kubectl cluster-info
kubectl api-resources
kubectl api-versions
kubectl get componentstatuses
kubectl get pods -n kube-system
kubectl describe node <node-name>
```

## Lab Ideas

- Trace a Deployment from YAML to ReplicaSet to Pod.
- Inspect `metadata.ownerReferences`.
- Compare namespaced and cluster-scoped resources.
- Inspect system Pods on EKS.

## Review Questions

1. What does the API server do?
2. Why is etcd critical?
3. What is the scheduler responsible for?
4. What is the kubelet responsible for?
5. What does reconciliation mean?
