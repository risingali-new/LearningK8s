# Sub-Session 02: Service Accounts And Deny By Default

This sub-session creates three ServiceAccounts and shows that creating an
identity does not automatically grant useful permissions.

## What This Lab Creates

```text
Namespace: rbac-lab

ServiceAccounts:
  dev-reader
  app-auditor
  platform-viewer
```

Each ServiceAccount represents a different job:

| ServiceAccount | Intended job |
| --- | --- |
| `dev-reader` | Read Pods and Deployments in one Namespace |
| `app-auditor` | Read common workload objects in one Namespace |
| `platform-viewer` | Read a cluster-scoped object later |

## Apply

From `sessions/14-rbac-and-identity`:

```bash
kubectl apply -f subsessions/02-service-accounts-and-deny-by-default/
```

## Check The Identities

```bash
kubectl get serviceaccounts -n rbac-lab
```

Set identity variables:

```bash
DEV_READER=system:serviceaccount:rbac-lab:dev-reader
APP_AUDITOR=system:serviceaccount:rbac-lab:app-auditor
PLATFORM_VIEWER=system:serviceaccount:rbac-lab:platform-viewer
```

Check permissions before any RoleBinding or ClusterRoleBinding exists:

```bash
kubectl auth can-i list pods -n rbac-lab --as="$DEV_READER"
kubectl auth can-i get secrets -n rbac-lab --as="$DEV_READER"
kubectl auth can-i list services -n rbac-lab --as="$APP_AUDITOR"
kubectl auth can-i list nodes --as="$PLATFORM_VIEWER"
```

Expected answer:

```text
no
no
no
no
```

This is the safest starting point. Kubernetes identities should receive only the
permissions they need.

## Cleanup

Run this only after the later sub-sessions are deleted:

```bash
kubectl delete -f subsessions/02-service-accounts-and-deny-by-default/ --ignore-not-found
```
