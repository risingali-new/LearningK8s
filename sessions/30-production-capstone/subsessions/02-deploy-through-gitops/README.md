# Sub-Session 02: Deploy Through GitOps

This sub-session makes Argo CD responsible for reconciling the capstone app.

## Goal

Create an Argo CD `Application` that points at the capstone package and keeps
the `message-board-prod` namespace in sync.

## App-Based Lab

Replace the repository URL with the Git repository that contains this training
repo, then apply the Argo CD application manifest.

```bash
kubectl apply -f subsessions/02-deploy-through-gitops/
```

## Check

```bash
kubectl get application -n argocd message-board-capstone
kubectl describe application -n argocd message-board-capstone
```

## Cleanup

```bash
kubectl delete -f subsessions/02-deploy-through-gitops/ --ignore-not-found
```

## Review Prompts

1. Which field tells Argo CD where the app manifests live?
2. Which namespace owns the Argo CD `Application` object?
3. Why should production deployments be reconciled from Git?
