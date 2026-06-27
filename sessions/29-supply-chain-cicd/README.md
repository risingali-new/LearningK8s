# Session 29: Supply Chain Security And CI/CD

This session connects application delivery to Kubernetes operations.

## Sub-Session Order

1. `01-image-build`: Dockerfile quality and reproducible builds.
2. `02-registry-flow`: ECR or Docker Hub tagging strategy.
3. `03-vulnerability-scanning`: scan images before deploy.
4. `04-sbom`: generate and store software bills of materials.
5. `05-image-signing`: cosign and signature verification.
6. `06-ci-pipeline`: GitHub Actions or Jenkins build pipeline.
7. `07-cd-handoff`: update Helm/Kustomize and let Argo CD deploy.
8. `08-promotion`: dev, stage, production release flow.

## Review Questions

1. Why should image tags be immutable?
2. What does an SBOM provide?
3. What problem does image signing solve?
4. Why should CI build and GitOps deploy be separate stages?
