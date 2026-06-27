# Sub-Session 02: PDB And VPA Safety

This sub-session shows how PodDisruptionBudget protects application availability during voluntary disruption.

## Why PDB Matters For Scaling

Autoscaling can cause disruption:

- VPA `Recreate` mode may evict Pods.
- Karpenter consolidation may drain Nodes.
- Cluster Autoscaler scale-down may drain Nodes.
- EKS managed node upgrades may drain Nodes.
- Manual `kubectl drain` evicts Pods.

A PodDisruptionBudget tells Kubernetes how many Pods must remain available during voluntary evictions.

## What PDB Does Not Protect Against

PDB does not prevent all outages.

It does not stop:

- Node hardware failure.
- Kernel crash.
- Network partition.
- Container crash.
- Forced deletion with `--force`.

It protects against voluntary evictions that use the Kubernetes Eviction API.

## Apply The Deployment And PDB

From `sessions/11-resource-management`:

```bash
kubectl apply -f subsessions/01-resource-guardrails/
kubectl apply -f subsessions/02-pdb-and-vpa-safety/01-safe-web-deployment.yml
kubectl apply -f subsessions/02-pdb-and-vpa-safety/02-safe-web-pdb.yml
```

Check:

```bash
kubectl get deployment safe-web -n app-scaling-prod
kubectl get pdb safe-web -n app-scaling-prod
kubectl describe pdb safe-web -n app-scaling-prod
```

The Deployment runs three replicas. The PDB uses:

```text
minAvailable: 2
```

That means one voluntary eviction is allowed, but Kubernetes should avoid voluntarily taking down two at the same time.

## Optional: VPA Recommendation Mode

If VPA is installed, apply recommendation mode:

```bash
kubectl apply -f subsessions/02-pdb-and-vpa-safety/03-safe-web-vpa-recommendation.yml
kubectl describe vpa safe-web -n app-scaling-prod
```

This is safe because `updateMode: "Off"` only writes recommendations.

## Optional: VPA Recreate Mode

Use this only after explaining evictions:

```bash
kubectl apply -f subsessions/02-pdb-and-vpa-safety/04-safe-web-vpa-recreate.yml
```

VPA updater should respect the PDB when evicting Pods. If evicting another Pod would violate `minAvailable`, eviction waits.

Watch:

```bash
kubectl get pods -n app-scaling-prod -l app=safe-web -w
kubectl describe pdb safe-web -n app-scaling-prod
```

## Drain Demonstration

Pick a node that has a `safe-web` Pod:

```bash
kubectl get pods -n app-scaling-prod -l app=safe-web -o wide
```

Drain carefully in a real lab cluster:

```bash
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

If the drain would violate the PDB, Kubernetes waits.

Uncordon after the demonstration:

```bash
kubectl uncordon <node-name>
```

## Cleanup

```bash
kubectl delete -f subsessions/02-pdb-and-vpa-safety/ --ignore-not-found
```

## Review Questions

1. What is a voluntary disruption?
2. Why does PDB matter with VPA `Recreate` mode?
3. Why does a single-replica app not get much protection from PDB?
4. Why is `minAvailable: 100%` dangerous during node maintenance?
5. How does PDB interact with node autoscaler scale-down?
