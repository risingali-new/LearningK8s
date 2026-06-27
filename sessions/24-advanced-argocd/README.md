# Session 24: Advanced Argo CD

This session moves from basic GitOps to production Argo CD patterns.

## Sub-Session Order

1. `01-application-manifests`: define Argo CD Applications as YAML.
2. `02-app-of-apps`: bootstrap many apps from one root app.
3. `03-applicationset`: generate apps from clusters or directories.
4. `04-sync-waves-and-hooks`: control ordering.
5. `05-helm-and-kustomize`: render common package formats.
6. `06-private-repos`: credentials and deploy keys.
7. `07-image-updater`: automated image tag updates.
8. `08-rbac-and-projects`: multi-team boundaries.

## Review Questions

1. Why manage Argo CD Applications in Git?
2. When is ApplicationSet better than app-of-apps?
3. What are sync waves useful for?
4. Why do AppProjects matter in multi-team clusters?
