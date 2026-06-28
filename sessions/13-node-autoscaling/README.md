# Session 13: Node Autoscaling

This session focuses on adding and removing cluster capacity when Pods cannot be
scheduled on existing Nodes.

## What This Session Covers

- Pending Pods as a capacity signal.
- Cluster Autoscaler.
- Karpenter.
- EKS Auto Mode.
- NodePools and NodeClaims.
- Cost and cleanup controls.

## Sub-Session Order

1. `subsessions/01-node-autoscaling`: Pending Pods, EKS Auto Mode, Karpenter, and Cluster Autoscaler patterns.

## Prerequisites

- Complete Session 10 so scheduling constraints are clear.
- Complete Session 11 so requests and limits are clear.
- Complete Session 12 so HPA behavior is clear.

## Useful Commands

```bash
kubectl get pods -A --field-selector=status.phase=Pending
kubectl describe pod <pod-name> -n <namespace>
kubectl get nodes
kubectl describe node <node-name>
kubectl get events -A --sort-by=.lastTimestamp
```

## Review Questions

1. Why does HPA need node capacity?
2. What causes a Pod to stay Pending?
3. How is Karpenter different from Cluster Autoscaler?
4. What does EKS Auto Mode manage for you?
