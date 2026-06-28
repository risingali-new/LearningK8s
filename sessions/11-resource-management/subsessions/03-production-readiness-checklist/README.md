# Sub-Session 03: Production Readiness Checklist

Use this checklist when reviewing a Kubernetes workload before production.

## 1. Workload Shape

Decide how the workload should scale:

| Workload | Common scaling choice |
| --- | --- |
| Stateless web/API | HPA + node autoscaling |
| Queue worker | HPA with queue depth or lag |
| Memory-heavy cache | Memory HPA or manual sizing |
| Stateful database | Careful manual scaling, VPA recommendations, storage planning |
| Batch jobs | Job parallelism, queue metrics, node autoscaling |
| Critical singleton | VPA recommendations, high availability redesign |

## 2. Requests And Limits

Every production container should have resource requests.

Check:

```bash
kubectl get deployment -n <namespace> <name> -o yaml
```

Look for:

```yaml
resources:
  requests:
    cpu: ...
    memory: ...
  limits:
    cpu: ...
    memory: ...
```

Rules of thumb:

- CPU request affects scheduling and CPU HPA percentages.
- Memory request affects scheduling and memory HPA percentages.
- CPU limit can throttle.
- Memory limit can cause OOM kill.
- Do not copy the same values everywhere. Measure and adjust.

## 3. Probes

Use probes so autoscaling and rollouts do not send traffic to unhealthy Pods.

Check:

- `startupProbe` for slow boot apps.
- `readinessProbe` for traffic eligibility.
- `livenessProbe` only when restart is the right recovery action.

## 4. HPA

Check:

```bash
kubectl get hpa -n <namespace>
kubectl describe hpa -n <namespace> <name>
```

Review:

- `minReplicas`.
- `maxReplicas`.
- Metric type.
- Target value.
- Scale-up behavior.
- Scale-down stabilization.
- Events.

Questions:

- Is the scaling metric actually correlated with user demand?
- Is `maxReplicas` high enough for peak load?
- Is `maxReplicas` low enough to protect dependencies?
- Can the database or downstream API handle the extra replicas?

## 5. VPA

Start with:

```text
updateMode: "Off"
```

Use VPA first as a recommendation engine.

Check:

```bash
kubectl describe vpa -n <namespace> <name>
```

Review:

- Target recommendation.
- Lower bound.
- Upper bound.
- Min/max policy.
- Whether automatic eviction is acceptable.

Avoid automatic CPU-changing VPA on the same workload as CPU-based HPA unless you have a deliberate design.

## 6. PDB

For replicated services, create a PodDisruptionBudget.

Check:

```bash
kubectl get pdb -n <namespace>
kubectl describe pdb -n <namespace> <name>
```

Rules of thumb:

- Single replica plus PDB does not provide high availability.
- `minAvailable: 100%` can block node drains.
- `maxUnavailable: 1` is common for small replicated web apps.
- PDB protects voluntary disruptions, not sudden failures.

## 7. Namespace Guardrails

Use:

- LimitRange for defaults and min/max values.
- ResourceQuota for total namespace caps.

Check:

```bash
kubectl describe limitrange -n <namespace>
kubectl describe resourcequota -n <namespace>
```

Questions:

- Can HPA scale to `maxReplicas` without hitting quota?
- Does quota protect the cluster from runaway scaling?
- Are default requests reasonable?

## 8. Node Autoscaling

Check whether Pending Pods can trigger new capacity.

```bash
kubectl get pods -A | grep Pending
kubectl describe pod -n <namespace> <pending-pod>
kubectl get nodes
```

For EKS:

- EKS Auto Mode: check `nodepools` and Auto Mode nodes.
- Karpenter: check `nodepools`, `nodeclaims`, and Karpenter controller logs.
- Cluster Autoscaler: check controller logs and Auto Scaling Group tags.

## 9. Scheduling Constraints

Review:

- Node selectors.
- Node affinity.
- Pod anti-affinity.
- Tolerations and taints.
- Topology spread constraints.
- PVC availability zone constraints.

Too many constraints can leave Pods Pending even when the cluster has enough total capacity.

## 10. Dependency Capacity

Scaling the application can overload dependencies.

Check:

- Database connection limits.
- Connection pool size.
- API rate limits.
- Message broker partitions.
- Cache capacity.
- Ingress or load balancer limits.

## 11. Observability

Before enabling aggressive autoscaling, observe:

- Pod CPU and memory.
- Replica count.
- Pending Pods.
- Node count.
- HPA decisions.
- VPA recommendations.
- Request rate.
- Error rate.
- Latency.
- Queue depth.
- Cost.

## 12. Load Test

Run a controlled test:

1. Start from normal traffic.
2. Increase traffic gradually.
3. Watch HPA scale-up.
4. Confirm new Pods become Ready.
5. Confirm node autoscaler adds capacity if needed.
6. Stop traffic.
7. Watch scale-down.
8. Confirm no dependency was overloaded.

## Troubleshooting Map

| Symptom | First checks |
| --- | --- |
| HPA target is `<unknown>` | Metrics Server, requests, `kubectl describe hpa` |
| HPA does not scale up | Metric below target, max replicas, missing metrics |
| Pods Pending | Node capacity, quota, affinity, taints, PVC zone |
| Node autoscaler does nothing | Autoscaler logs, ASG tags, NodePool requirements, IAM |
| VPA has no recommendations | Metrics Server, VPA pods, workload runtime |
| VPA evicts too much | PDB, update mode, min replicas |
| Costs jump | Inflate workload, high max replicas, node scale-down delay |

## Final Rule

Autoscaling is a control loop. Production safety comes from choosing the right signal, setting clear boundaries, and watching how the system behaves under real load.
