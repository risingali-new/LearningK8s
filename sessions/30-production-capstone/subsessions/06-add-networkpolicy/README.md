# Sub-Session 06: Add NetworkPolicy

This sub-session restricts app traffic to the paths the message board actually
needs.

## Goal

Allow frontend Pods to call the API services, and allow API Pods to call
PostgreSQL. Block unrelated same-namespace traffic.

## App-Based Lab

Use a CNI that enforces Kubernetes NetworkPolicy before applying this manifest.

```bash
kubectl apply -f subsessions/06-add-networkpolicy/
```

## Check

```bash
kubectl get networkpolicy -n message-board-prod
kubectl describe networkpolicy -n message-board-prod
```

## Cleanup

```bash
kubectl delete -f subsessions/06-add-networkpolicy/ --ignore-not-found
```

## Review Prompts

1. Which Pods are allowed to call the APIs?
2. Which Pods are allowed to call PostgreSQL?
3. What happens if the CNI does not enforce NetworkPolicy?
