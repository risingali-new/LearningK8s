# Sub-Session 06: PriorityClass And Preemption

This sub-session introduces scheduling priority.

## Concepts

PriorityClass gives Pods a numeric priority. When the cluster has scarce
capacity, the scheduler tries to schedule higher priority Pods first.

Preemption can happen when:

- a high-priority Pod cannot fit;
- lower-priority Pods are using capacity that would make room;
- preemption is allowed by policy;
- removing lower-priority Pods would let the high-priority Pod schedule.

Do not use very high priorities for normal application workloads. Kubernetes
reserves special priority values for critical system components.

## Apply

From `sessions/10-advanced-scheduling`:

```bash
kubectl apply -f subsessions/06-priority-and-preemption/01-priorityclasses.yml
kubectl apply -f subsessions/06-priority-and-preemption/02-low-priority-deployment.yml
kubectl apply -f subsessions/06-priority-and-preemption/03-high-priority-pod.yml
```

## Check

```bash
kubectl get priorityclass
kubectl get pods -n scheduling-lab -o wide
kubectl describe pod high-priority-demo -n scheduling-lab
```

This example is intentionally gentle. It demonstrates priority fields without
trying to force disruption on every lab cluster.

## Optional Preemption Demonstration

On a disposable cluster, increase the CPU request in
`03-high-priority-pod.yml` until the Pod cannot fit without evicting lower
priority Pods. Then inspect events:

```bash
kubectl describe pod high-priority-demo -n scheduling-lab
kubectl get events -n scheduling-lab --sort-by=.lastTimestamp
```

## Cleanup

```bash
kubectl delete -f subsessions/06-priority-and-preemption/ --ignore-not-found
```
