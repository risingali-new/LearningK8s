# Session 10: Advanced Scheduling

This session teaches how Kubernetes decides where Pods run after a workload is
created.

It fills the scheduling gap between core workloads and production autoscaling.
The same ideas appear later in node autoscaling, Karpenter, EKS Auto Mode, PDBs,
and cluster operations.

## What This Session Covers

- `nodeSelector`
- required and preferred node affinity
- pod affinity
- pod anti-affinity
- taints
- tolerations
- topology spread constraints
- PriorityClass
- preemption
- scheduler events and Pending Pod troubleshooting

## Mental Model

```text
User creates workload
  -> scheduler checks resource requests
  -> scheduler filters impossible Nodes
  -> scheduler scores possible Nodes
  -> scheduler binds the Pod to one Node
  -> kubelet starts the Pod on that Node
```

If no Node passes the scheduler filters, the Pod stays `Pending`.

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-prerequisites-and-namespace`: create the lab Namespace and inspect node labels.
2. `subsessions/02-node-selector-and-node-affinity`: pin Pods to labeled Nodes.
3. `subsessions/03-pod-affinity-and-anti-affinity`: place Pods near or away from other Pods.
4. `subsessions/04-taints-and-tolerations`: reserve Nodes and allow only tolerated Pods.
5. `subsessions/05-topology-spread`: distribute replicas across hostnames or zones.
6. `subsessions/06-priority-and-preemption`: influence scheduling when capacity is scarce.
7. `subsessions/07-scheduling-troubleshooting`: debug Pending Pods using events.

## Before You Start

Check the cluster:

```bash
kubectl get nodes -o wide
kubectl get nodes --show-labels
kubectl api-resources | grep -E "priorityclasses|pods|deployments"
```

Pick one worker node for the label and taint examples:

```bash
export SCHED_NODE=<node-name>
```

Label that node:

```bash
kubectl label node "$SCHED_NODE" training.k8s.io/node-role=scheduling-lab --overwrite
```

The taint lab later uses this same node.

## Full Apply Order

From `sessions/10-advanced-scheduling`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
kubectl apply -f subsessions/02-node-selector-and-node-affinity/01-node-selector-deployment.yml
kubectl apply -f subsessions/02-node-selector-and-node-affinity/02-required-node-affinity-deployment.yml
kubectl apply -f subsessions/02-node-selector-and-node-affinity/03-preferred-node-affinity-deployment.yml
kubectl apply -f subsessions/03-pod-affinity-and-anti-affinity/
kubectl apply -f subsessions/05-topology-spread/
kubectl apply -f subsessions/06-priority-and-preemption/
```

Run the taints and tolerations sub-session separately because it changes a Node:

```bash
kubectl taint node "$SCHED_NODE" training.k8s.io/dedicated=scheduling:NoSchedule --overwrite
kubectl apply -f subsessions/04-taints-and-tolerations/01-no-toleration-pod.yml
kubectl apply -f subsessions/04-taints-and-tolerations/02-toleration-pod.yml
```

## Useful Checks

```bash
kubectl get pods -n scheduling-lab -o wide
kubectl describe pod -n scheduling-lab <pod-name>
kubectl get events -n scheduling-lab --sort-by=.lastTimestamp
kubectl get priorityclass
```

## Cleanup

From `sessions/10-advanced-scheduling`:

```bash
kubectl delete -f subsessions/06-priority-and-preemption/ --ignore-not-found
kubectl delete -f subsessions/05-topology-spread/ --ignore-not-found
kubectl delete -f subsessions/04-taints-and-tolerations/ --ignore-not-found
kubectl delete -f subsessions/03-pod-affinity-and-anti-affinity/ --ignore-not-found
kubectl delete -f subsessions/02-node-selector-and-node-affinity/ --ignore-not-found
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
```

Remove the node label and taint:

```bash
kubectl taint node "$SCHED_NODE" training.k8s.io/dedicated=scheduling:NoSchedule-
kubectl label node "$SCHED_NODE" training.k8s.io/node-role-
```

## Review Questions

1. What is the difference between `nodeSelector` and node affinity?
2. Why can required affinity make Pods stay Pending?
3. What is the difference between pod affinity and pod anti-affinity?
4. Why does a taint repel Pods by default?
5. What does a toleration allow, and what does it not guarantee?
6. Why are topology spread constraints useful for production workloads?
7. When can preemption happen?
8. Which `kubectl` commands help explain a Pending Pod?
