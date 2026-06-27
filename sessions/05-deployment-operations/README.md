# Session 05: Deployment Operations

This session teaches safe day-to-day operation of Deployments.

## Sub-Session Order

1. `01-rollout-status`: watch Deployment rollout progress.
2. `02-rolling-update`: update image tags and observe ReplicaSets.
3. `03-rollout-history`: inspect revisions.
4. `04-rollback`: undo a bad release.
5. `05-recreate-strategy`: compare Recreate with RollingUpdate.
6. `06-graceful-shutdown`: termination grace period and zero-downtime releases.
7. `07-common-rollout-failures`: bad image, bad probe, bad config.

## Useful Commands

```bash
kubectl rollout status deployment/<name> -n <namespace>
kubectl rollout history deployment/<name> -n <namespace>
kubectl rollout undo deployment/<name> -n <namespace>
kubectl set image deployment/<name> <container>=<image> -n <namespace>
kubectl describe deployment <name> -n <namespace>
```

## Lab Ideas

- Roll a Deployment from one image tag to another.
- Break the image tag and watch rollout fail.
- Use `rollout undo`.
- Compare `maxSurge` and `maxUnavailable`.

## Review Questions

1. What creates a new Deployment revision?
2. What does `kubectl rollout undo` change?
3. Why do readiness probes matter during rolling updates?
4. When is `Recreate` acceptable?
