# Sub-Session 04: VPA Recommendations

This sub-session demonstrates Vertical Pod Autoscaler.

The lab creates:

- A `vpa-demo` Deployment.
- A `vpa-demo` ClusterIP Service.
- A `vpa-demo` VerticalPodAutoscaler in `Off` mode.
- A `vpa-load-generator` Deployment that continuously sends requests.

## How The Demo Works

The Deployment uses the same CPU-burning example image as the HPA lab:

```text
registry.k8s.io/hpa-example
```

This image is intentionally separate from the message-board images because the VPA lab needs a standalone CPU-load target without PostgreSQL dependencies.

The initial CPU request is intentionally small:

```yaml
cpu: 25m
memory: 64Mi
```

VPA watches usage and writes recommendations into:

```text
.status.recommendation
```

In `Off` mode, VPA does not change the running Pods. It only recommends.

## Apply The Workload

From `sessions/12-pod-autoscaling`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
kubectl apply -f subsessions/04-vpa-recommendations/01-vpa-demo-deployment.yml
```

Check:

```bash
kubectl get deployment vpa-demo -n app-autoscaling
kubectl get pods -n app-autoscaling -l app=vpa-demo
kubectl get service vpa-demo -n app-autoscaling
```

## Apply VPA In Recommendation Mode

```bash
kubectl apply -f subsessions/04-vpa-recommendations/02-vpa-recommendation-only.yml
```

Check:

```bash
kubectl get vpa -n app-autoscaling
kubectl describe vpa vpa-demo -n app-autoscaling
```

At first, recommendations may be empty. VPA needs metrics over time.

## Start Load

```bash
kubectl apply -f subsessions/04-vpa-recommendations/04-vpa-load-generator.yml
```

Watch metrics:

```bash
kubectl top pods -n app-autoscaling
```

Check recommendations:

```bash
kubectl describe vpa vpa-demo -n app-autoscaling
```

Important recommendation fields:

- `Lower Bound`: minimum suggested request.
- `Target`: recommended request for normal operation.
- `Upper Bound`: higher safe request based on observed usage.
- `Uncapped Target`: recommendation before min/max policy limits are applied.

## Optional: Apply Recommendations With Recreate

Do this only after students understand that VPA may evict Pods.

```bash
kubectl apply -f subsessions/04-vpa-recommendations/03-vpa-auto-recreate.yml
```

Delete a Pod so the Deployment creates a replacement:

```bash
kubectl delete pod -n app-autoscaling -l app=vpa-demo
kubectl get pods -n app-autoscaling -w
```

Inspect the new Pod resources:

```bash
kubectl get pod -n app-autoscaling -l app=vpa-demo -o jsonpath="{.items[0].spec.containers[0].resources}"
```

You should see requests influenced by the VPA recommendation.

## Stop Load

```bash
kubectl delete -f subsessions/04-vpa-recommendations/04-vpa-load-generator.yml --ignore-not-found
```

## Return VPA To Recommendation Mode

If you applied `Recreate` mode and want to return to safe mode:

```bash
kubectl apply -f subsessions/04-vpa-recommendations/02-vpa-recommendation-only.yml
```

## Cleanup

```bash
kubectl delete -f subsessions/04-vpa-recommendations/ --ignore-not-found
```

## Review Questions

1. Why does VPA need Metrics Server?
2. What does VPA write into its status?
3. What is the difference between `Off` and `Recreate` mode?
4. Why can `Recreate` mode cause application disruption?
5. Why should you start with VPA recommendations before applying changes automatically?
