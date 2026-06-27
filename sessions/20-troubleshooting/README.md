# Session 20: Troubleshooting

This session builds a repeatable debugging workflow.

## Sub-Session Order

1. `01-debugging-method`: observe, describe, isolate, fix, verify.
2. `02-pod-failures`: CrashLoopBackOff, ImagePullBackOff, CreateContainerConfigError.
3. `03-pending-pods`: resources, selectors, taints, PVCs, topology.
4. `04-service-and-dns`: no endpoints, wrong selector, CoreDNS issues.
5. `05-storage`: PVC Pending, mount failures, zone mismatch.
6. `06-network`: NetworkPolicy, CNI, kube-proxy, node routing.
7. `07-kubectl-debug`: ephemeral containers and node debug.
8. `08-runbooks`: write fixes as operational runbooks.

## Core Commands

```bash
kubectl get pods -A -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
kubectl get events -A --sort-by=.lastTimestamp
kubectl debug -it <pod-name> -n <namespace> --image=busybox
```

## Review Questions

1. Why should events be checked early?
2. What does `--previous` show in `kubectl logs`?
3. Why can DNS fail even when Pods are Running?
4. What is an ephemeral container useful for?
