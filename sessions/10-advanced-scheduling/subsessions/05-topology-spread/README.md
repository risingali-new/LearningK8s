# Sub-Session 05: Topology Spread Constraints

This sub-session teaches how to spread replicas across failure domains.

## Concepts

Topology spread constraints tell the scheduler:

```text
Try to keep matching Pods evenly spread across a topology.
```

Common topology keys:

- `kubernetes.io/hostname`: spread across Nodes.
- `topology.kubernetes.io/zone`: spread across availability zones.

## Apply

From `sessions/10-advanced-scheduling`:

```bash
kubectl apply -f subsessions/05-topology-spread/
```

## Check

```bash
kubectl get pods -n scheduling-lab -l app=topology-spread-web -o wide
kubectl describe deployment topology-spread-web -n scheduling-lab
```

The example uses `ScheduleAnyway`, so the scheduler prefers a balanced spread
but will still run the app on a small cluster.

## Try A Strict Constraint

Change `whenUnsatisfiable` to `DoNotSchedule` and increase replicas. On small
clusters, some Pods may stay Pending if the scheduler cannot satisfy the spread.

## Cleanup

```bash
kubectl delete -f subsessions/05-topology-spread/ --ignore-not-found
```
