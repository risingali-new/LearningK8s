# Sub-Session 07: Scheduling Troubleshooting

This sub-session gives a repeatable flow for debugging Pending Pods.

## First Checks

```bash
kubectl get pods -n scheduling-lab -o wide
kubectl describe pod -n scheduling-lab <pod-name>
kubectl get events -n scheduling-lab --sort-by=.lastTimestamp
```

The most useful scheduler information is usually in Pod events.

## Common Pending Reasons

| Symptom | What to check |
| --- | --- |
| Insufficient cpu or memory | Pod requests, node allocatable resources, quotas |
| Node selector mismatch | `nodeSelector`, node labels |
| Node affinity mismatch | required node affinity terms |
| Untolerated taint | Node taints and Pod tolerations |
| Volume node conflict | PVC zone and selected Node zone |
| Topology spread blocked | `maxSkew`, topology key, `DoNotSchedule` |
| Too many Pods | node pod density limits, CNI IP limits |
| Priority not enough | PriorityClass and lower-priority victims |

## Useful Commands

```bash
kubectl describe node <node-name>
kubectl top nodes
kubectl top pods -n scheduling-lab
kubectl get resourcequota -A
kubectl get limitrange -A
kubectl get pvc -A
kubectl get priorityclass
```

## Scheduler Event Phrases

Watch for messages such as:

```text
0/2 nodes are available: node(s) didn't match Pod's node affinity/selector.
0/2 nodes are available: node(s) had untolerated taint.
0/2 nodes are available: insufficient cpu.
preemption: No preemption victims found for incoming pod.
```

## Debugging Flow

```text
Pod Pending
  -> describe Pod
    -> read scheduler event
      -> check labels, taints, affinity, resources, PVCs, spread constraints
        -> fix the constraint or add capacity
```

## Review Questions

1. Why is `kubectl get pods` not enough for Pending Pod debugging?
2. Where does the scheduler explain failed placement?
3. What is the difference between a resource shortage and a label mismatch?
4. Why can a PVC keep a Pod Pending?
5. Why can autoscaling fail if scheduling constraints are too strict?
