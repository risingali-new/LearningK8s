# Session 07: Argo CD And GitOps

This session introduces Argo CD as a GitOps controller for Kubernetes.

The main teaching idea is:

```text
kubectl applies objects directly.
Argo CD watches a GitHub repository and applies what is stored there.
```

In this session, students do not create an Argo CD `Application` manifest with
`kubectl`. They create a normal GitHub repository, commit Kubernetes YAML into
it, and then use the Argo CD UI to connect that repository to the cluster.

## GitOps Flow

```text
Student GitHub repository
  -> manifests/app.yml
    -> Argo CD UI application points to repo + path
      -> Argo CD compares Git desired state with live Kubernetes state
        -> Sync applies the YAML from Git
```

## What Argo CD Teaches Here

| Idea | Meaning |
| --- | --- |
| Desired state | The YAML committed in GitHub |
| Live state | What is currently running in Kubernetes |
| OutOfSync | Git and the cluster do not match |
| Sync | Argo CD applies Git to the cluster |
| Self-heal | Argo CD fixes direct cluster changes that drift away from Git |
| Prune | Argo CD removes cluster objects that were removed from Git |

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-prerequisites-and-install`: install Argo CD and access the UI.
2. `subsessions/02-create-github-repository`: create a GitHub repository with sample Kubernetes YAML.
3. `subsessions/03-project-boundaries`: create a small Argo CD project boundary from the UI.
4. `subsessions/04-create-application-from-ui`: connect that GitHub repo from the Argo CD UI.
5. `subsessions/05-git-updates-and-auto-sync`: update Git, sync again, and test drift/self-heal.
6. `subsessions/06-cleanup`: remove the demo app and Argo CD.

## Prerequisites

For the full session:

- A working Kubernetes cluster.
- `kubectl` configured for that cluster.
- A GitHub account.
- Cluster outbound network access to GitHub.

Check the current cluster:

```bash
kubectl version
kubectl get nodes
kubectl get namespaces
```

## Target Shape By The End

```text
GitHub repository
  -> manifests/app.yml
    -> ConfigMap
    -> Deployment
    -> Service

argocd Namespace
  -> Argo CD control plane
  -> UI-created project named training-gitops
  -> UI-created application named argocd-demo

argocd-demo Namespace
  -> argocd-demo Deployment
  -> argocd-demo Service
```

## Install Argo CD

From `sessions/07-argocd`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-install/01-argocd-namespace.yml
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --for=condition=Available deployment/argocd-server -n argocd --timeout=180s
```

Then create the GitHub repository and Argo CD UI application from the next
sub-sessions.

## Useful Checks

```bash
kubectl get pods -n argocd
kubectl get all -n argocd-demo
```

Most Argo CD application work in this session happens in the browser UI.

## Cleanup

Use the Argo CD UI to delete the `argocd-demo` application first. Choose
cascading deletion if prompted so Argo CD removes the resources it created.

Then remove any remaining demo Namespace and Argo CD itself:

```bash
kubectl delete namespace argocd-demo --ignore-not-found
kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --ignore-not-found
kubectl delete -f subsessions/01-prerequisites-and-install/01-argocd-namespace.yml --ignore-not-found
```

## Review Questions

1. What is the source of truth in this GitOps workflow?
2. Why does Argo CD need both a Git repository URL and a path?
3. Why does Argo CD show an app as `OutOfSync`?
4. What is the difference between manual sync and automated sync?
5. What does self-heal do when someone edits a live Kubernetes object directly?
6. Why is prune useful, and why should it be enabled carefully?
7. Why should production installs pin an Argo CD version instead of using `stable`?

## References

- Argo CD getting started: `https://argo-cd.readthedocs.io/en/stable/getting_started/`
- Argo CD Application specification: `https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/`
- Argo CD sync options: `https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/`
