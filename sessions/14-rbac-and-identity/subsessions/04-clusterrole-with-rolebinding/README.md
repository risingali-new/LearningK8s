# Sub-Session 04: ClusterRole With RoleBinding

This sub-session shows how a ClusterRole can be reused inside one Namespace.

## Why This Pattern Exists

A `ClusterRole` is cluster-scoped, but not every use of a ClusterRole grants
cluster-wide access.

When a namespaced `RoleBinding` points to a `ClusterRole`, the permissions apply
only inside the RoleBinding's Namespace.

```text
ClusterRole workload-viewer
  -> reusable permission set

RoleBinding app-auditor-workload-viewer in rbac-lab
  -> grants that permission set only in rbac-lab
```

This is useful when many teams should receive the same read-only permission set
inside their own Namespaces.

## What This Lab Creates

```text
ClusterRole: workload-viewer
  allows:
    get/list/watch ConfigMaps, Endpoints, Pods, Services
    get/list/watch Deployments, ReplicaSets, StatefulSets, DaemonSets

RoleBinding: app-auditor-workload-viewer
  namespace: rbac-lab
  subject: ServiceAccount app-auditor
  roleRef: ClusterRole workload-viewer
```

## Apply

From `sessions/14-rbac-and-identity`:

```bash
kubectl apply -f subsessions/04-clusterrole-with-rolebinding/
```

## Inspect The Objects

```bash
kubectl describe clusterrole workload-viewer
kubectl describe rolebinding app-auditor-workload-viewer -n rbac-lab
```

## Check Namespace-Scoped Access

```bash
APP_AUDITOR=system:serviceaccount:rbac-lab:app-auditor

kubectl auth can-i list services -n rbac-lab --as="$APP_AUDITOR"
kubectl auth can-i list deployments.apps -n rbac-lab --as="$APP_AUDITOR"
kubectl auth can-i list configmaps -n rbac-lab --as="$APP_AUDITOR"
```

Expected answer:

```text
yes
yes
yes
```

## Check That Other Scopes Are Still Denied

```bash
kubectl auth can-i list services -n default --as="$APP_AUDITOR"
kubectl auth can-i list nodes --as="$APP_AUDITOR"
kubectl auth can-i get secrets -n rbac-lab --as="$APP_AUDITOR"
```

Expected answer:

```text
no
no
no
```

The ClusterRole is reusable, but the RoleBinding keeps this grant inside
`rbac-lab`.

## Cleanup

```bash
kubectl delete -f subsessions/04-clusterrole-with-rolebinding/ --ignore-not-found
```
