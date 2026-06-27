# Sub-Session 05: HPA And VPA Production Patterns

This sub-session is discussion-focused. Use it after students have seen both HPA and VPA in action.

## Comparison

| Topic | HPA | VPA |
| --- | --- | --- |
| Main action | Changes replica count | Changes or recommends CPU/memory requests |
| Native Kubernetes API | Yes | No, installed separately |
| Common target | Deployment, ReplicaSet, StatefulSet | Deployment, StatefulSet, DaemonSet, or other Pod controllers |
| Best fit | Stateless services with variable traffic | Right-sizing CPU and memory requests |
| Main risk | Too many Pods without enough node capacity | Pod eviction or request changes that affect scheduling |
| Metrics source | Metrics Server, custom metrics, external metrics | Metrics Server |

## When To Use HPA

Use HPA when:

- More Pods can handle more traffic.
- The app is stateless or stores state outside the Pod.
- The app has a Service or queue that can distribute work.
- You want fast response to load changes.

Examples:

- Web frontend.
- API service.
- Workers consuming queue messages.
- CPU-heavy stateless processors.

## When To Use VPA

Use VPA when:

- You do not know the correct CPU and memory requests.
- The workload cannot scale horizontally easily.
- You want recommendations before setting production requests.
- You want to reduce wasted resources from over-requested Pods.

Examples:

- Internal services with steady traffic.
- Stateful workloads where replica scaling needs care.
- Batch jobs.
- Recommendation-only sizing reports for production.

## When To Use Both

Use both carefully.

Safe patterns:

- HPA scales on custom or external metrics while VPA manages CPU and memory requests.
- HPA scales on CPU while VPA runs in `Off` mode only for recommendations.
- VPA manages memory recommendations while HPA scales on CPU or request rate, depending on the setup.

Risky pattern:

```text
HPA scales on CPU utilization.
VPA automatically changes CPU requests.
Both control the same signal.
```

This is risky because CPU utilization is calculated as:

```text
current CPU usage / requested CPU
```

If VPA changes the request, the value HPA sees also changes.

## Add Node Autoscaling

HPA and VPA only operate at the Pod level.

They do not create EC2 instances or Kubernetes Nodes.

If HPA creates more Pods than the cluster can schedule, Pods stay Pending:

```bash
kubectl get pods -n app-autoscaling
kubectl describe pod -n app-autoscaling <pending-pod-name>
```

Common production solution:

```text
HPA creates more Pods.
Cluster Autoscaler, Karpenter, or EKS Auto Mode adds more Nodes.
Scheduler places the new Pods.
```

## Resource Request Strategy

A practical production workflow:

1. Start with reasonable CPU and memory requests.
2. Install Metrics Server.
3. Use HPA for stateless services.
4. Run VPA in `Off` mode to collect recommendations.
5. Review VPA recommendations during normal and peak traffic.
6. Update Deployment requests manually or through a controlled release.
7. Add node autoscaling if HPA can exceed existing node capacity.

## Common Mistakes

- Creating CPU-based HPA without CPU requests.
- Setting `maxReplicas` too low and wondering why the app still struggles.
- Setting `maxReplicas` too high without node autoscaling.
- Enabling VPA `Recreate` mode on a critical service without disruption planning.
- Running HPA and VPA automatic CPU control on the same workload.
- Ignoring memory. HPA often reacts to CPU, but memory pressure can still cause OOM kills.

## Interview-Style Questions

1. What is the difference between horizontal and vertical scaling?
2. Why does HPA need Metrics Server?
3. Why does CPU-based HPA require CPU requests?
4. What happens when HPA wants six Pods but the cluster has room for only three?
5. What are the VPA components?
6. What VPA mode would you use first in production?
7. Why can VPA evict Pods?
8. How would you combine HPA, VPA, and node autoscaling safely?
