# Sub-Session 01: Resource Guardrails

This sub-session creates the Namespace and resource policies used by the production scaling labs.

## Why Guardrails Matter

Autoscaling creates more resource demand.

Without guardrails:

- One team can consume too much cluster capacity.
- A typo in `maxReplicas` can create too many Pods.
- Pods without resource requests can break HPA behavior.
- Pods without limits can consume more than expected.

Kubernetes gives two important namespace-level objects:

- `LimitRange`: sets defaults and min/max values for individual Pods or containers.
- `ResourceQuota`: caps aggregate resource usage in the Namespace.

## What This Lab Creates

```text
Namespace: app-scaling-prod
LimitRange: scaling-defaults
ResourceQuota: scaling-quota
```

The LimitRange sets default requests and limits so a Pod without explicit resources still gets reasonable values.

The ResourceQuota caps:

- Total Pods.
- Total requested CPU and memory.
- Total CPU and memory limits.
- Number of Services, LoadBalancers, PVCs, ConfigMaps, and Secrets.

## Apply

From `sessions/11-resource-management`:

```bash
kubectl apply -f subsessions/01-resource-guardrails/
```

## Check

```bash
kubectl get namespace app-scaling-prod
kubectl describe limitrange scaling-defaults -n app-scaling-prod
kubectl describe resourcequota scaling-quota -n app-scaling-prod
```

## Demonstrate Default Injection

Create a Pod without a `resources` block:

```bash
kubectl run no-resources-demo \
  -n app-scaling-prod \
  --image=nginx:1.27 \
  --restart=Never
```

Inspect the admitted Pod:

```bash
kubectl get pod no-resources-demo -n app-scaling-prod -o jsonpath="{.spec.containers[0].resources}"
```

The output should show defaults injected by the LimitRange.

Cleanup:

```bash
kubectl delete pod no-resources-demo -n app-scaling-prod --ignore-not-found
```

## Demonstrate Quota Protection

Try creating many replicas:

```bash
kubectl create deployment quota-test \
  -n app-scaling-prod \
  --image=nginx:1.27 \
  --replicas=60
```

Check:

```bash
kubectl describe deployment quota-test -n app-scaling-prod
kubectl describe resourcequota scaling-quota -n app-scaling-prod
kubectl get events -n app-scaling-prod --sort-by='.lastTimestamp'
```

The Deployment object may exist, but not all Pods will be admitted if the quota would be exceeded.

Cleanup:

```bash
kubectl delete deployment quota-test -n app-scaling-prod --ignore-not-found
```

## Cleanup

Only delete this sub-session after all Session 11 labs are finished:

```bash
kubectl delete -f subsessions/01-resource-guardrails/ --ignore-not-found
```

## Review Questions

1. What is the difference between LimitRange and ResourceQuota?
2. Why does HPA need resource requests?
3. What happens when a Deployment tries to create Pods beyond quota?
4. Why is a namespace-level quota useful in a shared cluster?
