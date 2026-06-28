# Sub-Session 04: Create Application From The Argo CD UI

This sub-session connects the GitHub repository to Argo CD using the web UI.

By the end, Argo CD should know:

```text
Which repo to read
Which folder in that repo contains YAML
Which project boundary to use
Which cluster and Namespace to deploy into
```

## Open The Argo CD UI

Start a port-forward if it is not already running:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open:

```text
https://localhost:8080
```

Login as `admin` using the password from sub-session 01.

## Create The Application

In the Argo CD UI, choose:

```text
NEW APP
```

Use these values:

| Field | Value |
| --- | --- |
| Application Name | `argocd-demo` |
| Project Name | `training-gitops` |
| Sync Policy | `Manual` |
| Repository URL | `https://github.com/<GITHUB_USERNAME>/argocd-demo-app.git` |
| Revision | `HEAD` |
| Path | `manifests` |
| Cluster URL | `https://kubernetes.default.svc` |
| Namespace | `argocd-demo` |
| Directory Recurse | Disabled |
| Sync Option | Enable `Create Namespace` or `Auto-create namespace` if shown |

Replace `<GITHUB_USERNAME>` with the student's GitHub username.

If the project boundary sub-session was skipped, use `default` as the project
name instead.

Create the app.

## First Status

The app should appear in the UI.

Before the first sync, it may show:

```text
OutOfSync
```

That is expected. Argo CD can see the desired state in GitHub, but it has not
applied it to Kubernetes yet.

## Sync From The UI

Open the `argocd-demo` app and choose:

```text
SYNC
```

Confirm the sync.

After a successful sync, the app should move toward:

```text
Synced
Healthy
```

## Check In Kubernetes

```bash
kubectl get namespace argocd-demo
kubectl get all -n argocd-demo
```

Port-forward the demo app:

```bash
kubectl port-forward service/argocd-demo -n argocd-demo 8081:80
```

Open:

```text
http://localhost:8081
```

## Important Detail

The Argo CD UI creates an Argo CD application behind the scenes. The teaching
workflow is still UI-first:

```text
GitHub repo contains Kubernetes YAML.
Argo CD UI points to the repo.
Argo CD syncs the repo into Kubernetes.
```

## Review Questions

1. Which UI field tells Argo CD where the GitHub repository is?
2. Why is the path `manifests` instead of the repository root?
3. Why does the app use the `training-gitops` project?
4. Why does the app start as `OutOfSync`?
5. What changed in Kubernetes after pressing `SYNC`?
