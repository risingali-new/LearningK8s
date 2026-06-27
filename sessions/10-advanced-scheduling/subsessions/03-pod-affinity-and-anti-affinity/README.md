# Sub-Session 03: Pod Affinity And Anti-Affinity

This sub-session teaches placement based on other Pods instead of Node labels.

## Concepts

Pod affinity says:

```text
Prefer or require this Pod near Pods matching these labels.
```

Pod anti-affinity says:

```text
Prefer or require this Pod away from Pods matching these labels.
```

The `topologyKey` controls what "near" or "away" means. Common values are:

- `kubernetes.io/hostname`
- `topology.kubernetes.io/zone`

## Apply

From `sessions/10-advanced-scheduling`:

```bash
kubectl apply -f subsessions/03-pod-affinity-and-anti-affinity/
```

## Check

```bash
kubectl get pods -n scheduling-lab -o wide
kubectl describe pod -n scheduling-lab -l app=affinity-client
kubectl describe pod -n scheduling-lab -l app=anti-affinity-web
```

The affinity client prefers to run on the same hostname as the cache Pod. The
web Deployment prefers to spread replicas across hostnames.

These examples use preferred rules so they remain safe on small clusters.

## Cleanup

```bash
kubectl delete -f subsessions/03-pod-affinity-and-anti-affinity/ --ignore-not-found
```
