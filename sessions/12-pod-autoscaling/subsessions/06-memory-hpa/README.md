# Sub-Session 06: Memory-Based HPA

This sub-session demonstrates HPA using memory utilization.

## CPU HPA vs Memory HPA

CPU often rises and falls quickly. CPU-based HPA can react well to traffic spikes.

Memory behaves differently:

- Memory can grow slowly.
- Many runtimes do not immediately release memory to the operating system.
- Memory pressure may not fall quickly after traffic stops.
- Memory-based scale-down can be slower and less predictable.

Use memory HPA when memory consumption truly correlates with load, such as cache-heavy or request-buffer-heavy applications.

## What This Lab Creates

- `memory-demo` Deployment.
- `memory-demo` Service.
- `memory-demo` HPA based on average memory utilization.
- `memory-load-generator` Deployment.

The app allocates memory when `/allocate` is called.

## Apply

From `sessions/12-pod-autoscaling`:

```bash
kubectl apply -f subsessions/01-resource-guardrails/
kubectl apply -f subsessions/06-memory-hpa/01-memory-demo-deployment.yml
kubectl apply -f subsessions/06-memory-hpa/02-memory-demo-hpa.yml
kubectl apply -f subsessions/06-memory-hpa/03-memory-load-generator.yml
```

## Watch

```bash
kubectl get hpa memory-demo -n app-scaling-prod -w
```

In another terminal:

```bash
kubectl top pods -n app-scaling-prod
kubectl get deployment memory-demo -n app-scaling-prod -w
```

Expected behavior:

- The load generator calls `/allocate`.
- Pod memory rises.
- HPA increases replicas when average memory utilization rises above target.

## Inspect The HPA

```bash
kubectl describe hpa memory-demo -n app-scaling-prod
```

Important fields:

- Current memory utilization.
- Target memory utilization.
- HPA conditions.
- Recent scaling events.

## Release Memory

The app has a `/release` endpoint:

```bash
kubectl run release-memory \
  -n app-scaling-prod \
  --image=busybox:1.36 \
  --restart=Never \
  --rm -it \
  -- wget -q -O- http://memory-demo/release
```

Then stop load:

```bash
kubectl delete -f subsessions/06-memory-hpa/03-memory-load-generator.yml --ignore-not-found
```

HPA scale-down may still take time because of stabilization and because memory usage may not drop immediately.

## Cleanup

```bash
kubectl delete -f subsessions/06-memory-hpa/ --ignore-not-found
```

## Review Questions

1. Why does memory HPA need memory requests?
2. Why can memory scale-down be slower than CPU scale-down?
3. When is memory a good scaling signal?
4. Why should you keep `maxReplicas` conservative?
