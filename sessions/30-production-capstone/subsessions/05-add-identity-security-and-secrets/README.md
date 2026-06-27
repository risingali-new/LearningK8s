# Sub-Session 05: Add Identity, Security, And Secrets

This sub-session adds runtime identities and moves database credentials toward a
managed secret workflow.

## Goal

Create least-privilege ServiceAccounts, bind read-only discovery permissions,
and define an External Secrets Operator flow for the app database Secret.

## App-Based Lab

Install External Secrets Operator before applying this manifest. Replace the AWS
region, External Secrets ServiceAccount setup, and remote secret names with your
own values.

```bash
kubectl apply -f subsessions/05-add-identity-security-and-secrets/
```

## Check

```bash
kubectl get serviceaccount,role,rolebinding -n message-board-prod
kubectl get externalsecret -n message-board-prod
kubectl describe externalsecret -n message-board-prod app-db-secret
```

## Cleanup

```bash
kubectl delete -f subsessions/05-add-identity-security-and-secrets/ --ignore-not-found
```

## Review Prompts

1. Which identity should each app tier use?
2. Why should production credentials not live directly in Git?
3. What should be audited when a secret rotates?
