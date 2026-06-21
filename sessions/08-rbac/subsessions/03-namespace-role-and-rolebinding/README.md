# Sub-Session 03: Namespace Role And RoleBinding

This sub-session grants a ServiceAccount read-only access in one Namespace.

## What This Lab Creates

```text
Role: pod-reader
  namespace: rbac-lab
  allows:
    get/list/watch Pods
    get Pod logs
    get/list/watch Deployments

RoleBinding: dev-reader-pod-reader
  namespace: rbac-lab
  subject: ServiceAccount dev-reader
  roleRef: Role pod-reader
```

## Apply

From `sessions/08-rbac`:

```bash
kubectl apply -f subsessions/03-namespace-role-and-rolebinding/
```

## Inspect The RBAC Objects

```bash
kubectl describe role pod-reader -n rbac-lab
kubectl describe rolebinding dev-reader-pod-reader -n rbac-lab
```

## Check What Is Allowed

```bash
DEV_READER=system:serviceaccount:rbac-lab:dev-reader

kubectl auth can-i list pods -n rbac-lab --as="$DEV_READER"
kubectl auth can-i get pods --subresource=log -n rbac-lab --as="$DEV_READER"
kubectl auth can-i list deployments.apps -n rbac-lab --as="$DEV_READER"
```

Expected answer:

```text
yes
yes
yes
```

## Check What Is Still Denied

```bash
kubectl auth can-i delete pods -n rbac-lab --as="$DEV_READER"
kubectl auth can-i create deployments.apps -n rbac-lab --as="$DEV_READER"
kubectl auth can-i get secrets -n rbac-lab --as="$DEV_READER"
kubectl auth can-i list pods -n default --as="$DEV_READER"
```

Expected answer:

```text
no
no
no
no
```

The RoleBinding grants access only in `rbac-lab`. It does not grant access in
`default` or any other Namespace.

## Important Detail

`roleRef` is immutable. If a RoleBinding points to the wrong Role, delete and
recreate the RoleBinding instead of trying to edit `roleRef`.

## Cleanup

Run this only after later sub-sessions that depend on the ServiceAccounts:

```bash
kubectl delete -f subsessions/03-namespace-role-and-rolebinding/ --ignore-not-found
```
