# Sub-Session 01: Package The App

This sub-session turns the training message board into the base production
workload for the capstone.

## Goal

Create the `message-board-prod` namespace and deploy the frontend, user API,
app API, PostgreSQL backing service, ConfigMap, Secret, and internal Services.

## App-Based Lab

Apply the base package first. Later capstone sub-sessions layer GitOps, ingress,
security, policy, and observability on top of these same app resources.

```bash
kubectl apply -f subsessions/01-package-the-app/
```

## Check

```bash
kubectl get all -n message-board-prod
kubectl get endpoints -n message-board-prod
kubectl logs -n message-board-prod deployment/frontend
```

## Cleanup

```bash
kubectl delete -f subsessions/01-package-the-app/ --ignore-not-found
```

## Review Prompts

1. Which resources are application code, and which resources are platform glue?
2. Which Services are internal only?
3. What should be changed before treating the database as production data?
