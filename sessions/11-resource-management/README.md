# Session 11: Resource Management And Disruption Safety

This session teaches how Kubernetes protects cluster capacity and workload
availability.

## What This Session Covers

- CPU and memory requests.
- CPU and memory limits.
- QoS classes.
- OOMKilled and eviction.
- LimitRange defaults and min/max rules.
- ResourceQuota namespace caps.
- PodDisruptionBudget.
- Production readiness checks.

## Sub-Session Order

1. `subsessions/01-resource-guardrails`: Namespace, LimitRange, and ResourceQuota.
2. `subsessions/02-pdb-and-vpa-safety`: PodDisruptionBudget and voluntary evictions.
3. `subsessions/03-production-readiness-checklist`: production scaling and readiness checklist.

## Useful Commands

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl top pods -n <namespace>
kubectl get resourcequota -A
kubectl get limitrange -A
kubectl get pdb -A
kubectl describe node <node-name>
```

## Review Questions

1. What is the difference between a request and a limit?
2. How does QoS affect eviction order?
3. Why can a ResourceQuota block new Pods?
4. What kind of disruption does a PDB protect against?
5. Why do requests affect scheduling and HPA behavior?
