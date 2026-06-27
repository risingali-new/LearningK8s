# Sub-Session 03: Project Boundaries

This sub-session creates a small Argo CD project from the UI.

An Argo CD project controls where an application is allowed to deploy from and
where it is allowed to deploy to. For this lab, the boundary is intentionally
simple:

```text
Only this student's GitHub repo
Only the in-cluster Kubernetes API
Only the argocd-demo Namespace
```

## Open Project Settings

In the Argo CD UI, go to:

```text
Settings -> Projects
```

Choose:

```text
NEW PROJECT
```

## Create The Project

Use these values:

| Field | Value |
| --- | --- |
| Name | `training-gitops` |
| Description | `Training project for the Argo CD GitHub demo` |

Save the project.

## Add The Source Repository

Inside the `training-gitops` project, add an allowed source repository:

```text
https://github.com/<GITHUB_USERNAME>/argocd-demo-app.git
```

Replace `<GITHUB_USERNAME>` with the student's GitHub username.

This means applications in this project can read manifests only from that
repository.

## Add The Destination

Add this allowed destination:

| Field | Value |
| --- | --- |
| Server | `https://kubernetes.default.svc` |
| Namespace | `argocd-demo` |

This means applications in this project can deploy only into the `argocd-demo`
Namespace on the same cluster where Argo CD is running.

## Keep Resource Rules Simple

The sample app contains only namespaced resources:

```text
ConfigMap
Deployment
Service
```

The next sub-session uses Argo CD's `Create Namespace` sync option to create
`argocd-demo` if it is missing. That keeps the project boundary focused on repo
and destination instead of cluster-scoped resource permissions.

## Why This Matters

The default Argo CD project is useful for quick testing, but it is broad. A
dedicated project lets teams keep applications inside an expected area:

```text
Repo boundary + namespace boundary = smaller blast radius
```

In production, combine Argo CD projects with:

```text
GitHub permissions
Argo CD RBAC
Kubernetes RBAC
Cloud IAM
```

## Review Questions

1. What does an Argo CD project restrict?
2. Why is the source repository limited to one GitHub repo?
3. Why is the destination Namespace limited to `argocd-demo`?
4. Why is the default project convenient but risky?
