# Session 14: RBAC And Service Account Permissions

This session introduces Kubernetes Role-Based Access Control.

The main teaching idea is:

```text
Authentication answers: who are you?
Authorization answers: what are you allowed to do?
RBAC answers authorization with Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings.
```

In this session, students create ServiceAccounts, prove that they have no useful
permissions by default, then grant least-privilege access one step at a time.

## RBAC Building Blocks

| Object | Scope | Main use |
| --- | --- | --- |
| ServiceAccount | Namespace | Identity used by Pods and automation inside Kubernetes |
| Role | Namespace | Permissions for namespaced resources in one Namespace |
| RoleBinding | Namespace | Connects a user, group, or ServiceAccount to a Role or ClusterRole in one Namespace |
| ClusterRole | Cluster | Reusable permission set, or permissions for cluster-scoped resources |
| ClusterRoleBinding | Cluster | Connects a subject to a ClusterRole across the whole cluster |

## Important Mental Model

```text
Subject
  -> ServiceAccount, user, or group
    -> bound by RoleBinding or ClusterRoleBinding
      -> to Role or ClusterRole
        -> which allows verbs on resources
```

Example:

```text
system:serviceaccount:rbac-lab:dev-reader
  -> RoleBinding in rbac-lab
    -> Role named pod-reader
      -> can get/list/watch Pods in rbac-lab
```

## RBAC Is Not EKS IAM

On EKS, there are two permission systems that often appear together:

- AWS IAM controls access to AWS APIs.
- Kubernetes RBAC controls access to the Kubernetes API.

IAM Roles for Service Accounts can let a Pod call AWS services. RBAC lets that
same Pod call Kubernetes resources such as Pods, Services, ConfigMaps, Nodes,
and Deployments.

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-prerequisites-and-namespace`: create the RBAC lab Namespace.
2. `subsessions/02-service-accounts-and-deny-by-default`: create identities and inspect default denial.
3. `subsessions/03-namespace-role-and-rolebinding`: grant namespaced read access with a Role.
4. `subsessions/04-clusterrole-with-rolebinding`: reuse a ClusterRole inside one Namespace.
5. `subsessions/05-clusterrolebinding-for-cluster-scope`: grant cluster-scoped read access carefully.

## Prerequisites

You need:

- A working Kubernetes cluster.
- `kubectl` configured.
- A current identity with permission to create RBAC objects.
- Permission to impersonate ServiceAccounts for `kubectl auth can-i --as=...`
  checks. A cluster-admin style training identity normally has this.

Check the current cluster and your own permissions:

```bash
kubectl version
kubectl get nodes
kubectl auth can-i create roles -n default
kubectl auth can-i create clusterroles
kubectl auth can-i impersonate serviceaccounts
```

## Target Shape By The End

```text
rbac-lab Namespace

ServiceAccounts:
  dev-reader
  app-auditor
  platform-viewer

Role:
  pod-reader
    -> read Pods, Pod logs, and Deployments in rbac-lab

RoleBinding:
  dev-reader-pod-reader
    -> grants dev-reader the pod-reader Role in rbac-lab

ClusterRole:
  workload-viewer
    -> read common namespaced workload resources

RoleBinding:
  app-auditor-workload-viewer
    -> grants app-auditor workload-viewer only in rbac-lab

ClusterRole:
  node-reader
    -> read Nodes

ClusterRoleBinding:
  platform-viewer-node-reader
    -> grants platform-viewer node read access across the cluster
```

## Full Apply Order

From `sessions/14-rbac-and-identity`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
kubectl apply -f subsessions/02-service-accounts-and-deny-by-default/
kubectl apply -f subsessions/03-namespace-role-and-rolebinding/
kubectl apply -f subsessions/04-clusterrole-with-rolebinding/
kubectl apply -f subsessions/05-clusterrolebinding-for-cluster-scope/
```

Set useful identity variables:

```bash
DEV_READER=system:serviceaccount:rbac-lab:dev-reader
APP_AUDITOR=system:serviceaccount:rbac-lab:app-auditor
PLATFORM_VIEWER=system:serviceaccount:rbac-lab:platform-viewer
```

Check the final permissions:

```bash
kubectl auth can-i list pods -n rbac-lab --as="$DEV_READER"
kubectl auth can-i delete pods -n rbac-lab --as="$DEV_READER"

kubectl auth can-i list services -n rbac-lab --as="$APP_AUDITOR"
kubectl auth can-i list services -n default --as="$APP_AUDITOR"

kubectl auth can-i list nodes --as="$PLATFORM_VIEWER"
kubectl auth can-i list pods --all-namespaces --as="$PLATFORM_VIEWER"
```

Expected pattern:

```text
dev-reader:      can read selected objects in rbac-lab, cannot delete them.
app-auditor:     can read selected namespaced resources only in rbac-lab.
platform-viewer: can read Nodes, but not Pods across all Namespaces.
```

## Cleanup

From `sessions/14-rbac-and-identity`:

```bash
kubectl delete -f subsessions/05-clusterrolebinding-for-cluster-scope/ --ignore-not-found
kubectl delete -f subsessions/04-clusterrole-with-rolebinding/ --ignore-not-found
kubectl delete -f subsessions/03-namespace-role-and-rolebinding/ --ignore-not-found
kubectl delete -f subsessions/02-service-accounts-and-deny-by-default/ --ignore-not-found
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
```

## Review Questions

1. What is the difference between authentication and authorization?
2. Why should most application Pods use a dedicated ServiceAccount?
3. What is the difference between a Role and a ClusterRole?
4. What is the difference between a RoleBinding and a ClusterRoleBinding?
5. Why does a RoleBinding to a ClusterRole still only grant access in one Namespace?
6. Why is granting `get`, `list`, and `watch` safer than granting `*`?
7. Why should access to Secrets be treated carefully?
8. Why should ClusterRoleBindings be reviewed more carefully than RoleBindings?
9. In EKS, what is the difference between Kubernetes RBAC and AWS IAM?

## References

- Kubernetes RBAC documentation: `https://kubernetes.io/docs/reference/access-authn-authz/rbac/`
- Kubernetes ServiceAccount documentation: `https://kubernetes.io/docs/concepts/security/service-accounts/`
- Kubernetes authorization overview: `https://kubernetes.io/docs/reference/access-authn-authz/authorization/`
- Kubernetes `kubectl auth can-i`: `https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/`
