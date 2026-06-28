# Sub-Session 08: Run Failure Drills

This sub-session verifies that the capstone app behaves predictably when common
production failures happen.

## Goal

Practice restart, rollout, rollback, node maintenance, service dependency, and
secret rotation drills.

## App-Based Lab

Run each drill against the `message-board-prod` app and record the command,
expected symptom, recovery signal, and rollback path.

```bash
kubectl rollout restart deployment/frontend -n message-board-prod
kubectl rollout status deployment/frontend -n message-board-prod
kubectl scale deployment app-service -n message-board-prod --replicas=0
kubectl get events -n message-board-prod --sort-by=.lastTimestamp
kubectl scale deployment app-service -n message-board-prod --replicas=2
```

## Check

```bash
kubectl get pods -n message-board-prod -o wide
kubectl get pdb -n message-board-prod
kubectl logs -n message-board-prod deployment/frontend
```

## Cleanup

```bash
kubectl scale deployment app-service -n message-board-prod --replicas=2
kubectl scale deployment user-service -n message-board-prod --replicas=2
kubectl rollout status deployment/frontend -n message-board-prod
```

## Review Prompts

1. Which failure was visible to users?
2. Which failure was only visible in telemetry?
3. Which recovery action should be automated?
