# Sub-Session 05: ClusterRoleBinding For Cluster Scope

This sub-session grants a ServiceAccount read-only access to a cluster-scoped
resource.

## Why ClusterRoleBinding Needs Care

A `ClusterRoleBinding` grants access across the cluster. It is the right tool
for cluster-scoped resources such as Nodes, but it should be reviewed carefully.

This lab grants only Node read access:

```text
ClusterRole node-reader
  -> get/list/watch Nodes

ClusterRoleBinding platform-viewer-node-reader
  -> ServiceAccount platform-viewer can read Nodes
```

It does not grant broad access to Pods, Secrets, or Deployments.

## Apply

From `sessions/08-rbac`:

```bash
kubectl apply -f subsessions/05-clusterrolebinding-for-cluster-scope/
```

## Inspect The Objects

```bash
kubectl describe clusterrole node-reader
kubectl describe clusterrolebinding platform-viewer-node-reader
```

## Check Cluster-Scoped Access

```bash
PLATFORM_VIEWER=system:serviceaccount:rbac-lab:platform-viewer

kubectl auth can-i list nodes --as="$PLATFORM_VIEWER"
kubectl auth can-i get nodes --as="$PLATFORM_VIEWER"
```

Expected answer:

```text
yes
yes
```

## Check That Broad Workload Access Is Still Denied

```bash
kubectl auth can-i list pods --all-namespaces --as="$PLATFORM_VIEWER"
kubectl auth can-i list secrets --all-namespaces --as="$PLATFORM_VIEWER"
kubectl auth can-i create deployments.apps -n rbac-lab --as="$PLATFORM_VIEWER"
```

Expected answer:

```text
no
no
no
```

## Important Production Habit

Avoid using `cluster-admin` for application workloads. If a workload needs
cluster-level visibility, write the smallest possible ClusterRole and bind only
the identity that needs it.

## Cleanup

```bash
kubectl delete -f subsessions/05-clusterrolebinding-for-cluster-scope/ --ignore-not-found
```
