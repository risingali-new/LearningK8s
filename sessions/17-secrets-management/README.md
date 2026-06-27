# Session 17: Secrets Management

This session moves beyond plain Kubernetes Secret objects.

## Sub-Session Order

1. `01-kubernetes-secrets-review`: base64 encoding, mounts, env vars.
2. `02-secret-risks`: etcd, RBAC, logs, manifests, Git.
3. `03-external-secrets-operator`: sync from AWS Secrets Manager.
4. `04-secrets-store-csi-driver`: mount secrets directly from providers.
5. `05-sealed-secrets`: encrypted Secret manifests.
6. `06-sops`: Git-friendly encrypted config.
7. `07-rotation-and-audit`: rotation patterns and access review.

## Review Questions

1. Why is base64 not encryption?
2. Why should raw Secrets not be committed to Git?
3. When would you use External Secrets Operator?
4. When would you use SOPS or Sealed Secrets?
