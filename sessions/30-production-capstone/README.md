# Session 30: Production Capstone

This final session combines the full course into one production-style delivery.

## Capstone Goal

Deploy the sample application with:

- Helm or Kustomize packaging.
- Argo CD GitOps deployment.
- Ingress or Gateway API with TLS.
- RBAC and least-privilege ServiceAccounts.
- Secret management.
- Resource requests, limits, quota, and PDBs.
- HPA and node autoscaling readiness.
- NetworkPolicy.
- Observability dashboards and alerts.
- Backup and restore plan.
- Troubleshooting runbook.

## Sub-Session Order

1. `subsessions/01-package-the-app`: Create the production namespace and package the message board app stack.
2. `subsessions/02-deploy-through-gitops`: Register the capstone app with Argo CD.
3. `subsessions/03-add-tls-and-dns`: Expose the app through Gateway API with TLS.
4. `subsessions/04-add-resource-and-scheduling-controls`: Add replicas, resource requests, topology spread, and PDBs.
5. `subsessions/05-add-identity-security-and-secrets`: Add runtime identities and externalized secrets.
6. `subsessions/06-add-networkpolicy`: Restrict east-west traffic between the app services.
7. `subsessions/07-add-metrics-logs-and-alerts`: Add metrics discovery and a starter alert.
8. `subsessions/08-run-failure-drills`: Practice failure, rollback, drain, and recovery drills.
9. `subsessions/09-document-production-readiness`: Finish the production readiness review.

## Suggested Milestones

1. Package the app.
2. Deploy through GitOps.
3. Add TLS and DNS.
4. Add resource and scheduling controls.
5. Add identity, security, and secrets.
6. Add NetworkPolicy.
7. Add metrics, logs, and alerts.
8. Run failure drills.
9. Document production readiness.

## Final Review

1. Can the app survive a Pod restart?
2. Can the team roll back a bad release?
3. Can traffic stay available during a node drain?
4. Can alerts explain user-impacting failure?
5. Can a new engineer understand the runbook?
