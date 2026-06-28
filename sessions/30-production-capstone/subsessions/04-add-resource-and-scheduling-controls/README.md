# Sub-Session 04: Add Resource And Scheduling Controls

This sub-session makes the frontend safer during scaling and maintenance.

## Goal

Add replicas, resource requests and limits, topology spreading, and a
PodDisruptionBudget for the frontend.

## App-Based Lab

Run this after the base app stack so the frontend Deployment already exists.

```bash
kubectl apply -f subsessions/04-add-resource-and-scheduling-controls/
```

## Check

```bash
kubectl get deployment frontend -n message-board-prod
kubectl describe deployment frontend -n message-board-prod
kubectl get pdb -n message-board-prod
```

## Cleanup

```bash
kubectl delete -f subsessions/04-add-resource-and-scheduling-controls/ --ignore-not-found
```

## Review Prompts

1. How do requests influence scheduling?
2. What happens if one node drains while the PDB is active?
3. Why is topology spread useful for the frontend?
