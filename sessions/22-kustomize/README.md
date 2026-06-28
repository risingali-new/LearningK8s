# Session 22: Kustomize

This session teaches environment overlays without templating.

## Sub-Session Order

1. `01-kustomize-concepts`: base, overlay, resource, patch.
2. `02-create-base`: common app manifests.
3. `03-dev-overlay`: small replicas and local settings.
4. `04-prod-overlay`: production labels, replicas, resources.
5. `05-patches`: strategic merge and JSON patches.
6. `06-configmap-secret-generators`: generated config.
7. `07-kustomize-with-kubectl-and-argocd`: apply and GitOps usage.

## Useful Commands

```bash
kubectl kustomize overlays/dev
kubectl apply -k overlays/dev
kubectl diff -k overlays/prod
```

## Review Questions

1. How is Kustomize different from Helm?
2. What belongs in a base?
3. What belongs in an overlay?
4. Why are overlays useful for GitOps?
