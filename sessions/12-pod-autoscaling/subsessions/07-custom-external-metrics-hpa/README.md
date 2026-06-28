# Sub-Session 07: Custom And External Metrics HPA

This sub-session explains HPA with custom and external metrics.

CPU and memory are resource metrics. They are useful, but they do not always describe user demand.

Better production signals can be:

- HTTP requests per second.
- Queue depth.
- Jobs waiting.
- Messages visible in SQS.
- Active websocket sessions.
- Checkout latency.
- Business events per minute.

## Metric Types In HPA v2

`autoscaling/v2` supports:

- `Resource`: CPU or memory from Metrics Server.
- `ContainerResource`: CPU or memory for one named container.
- `Pods`: one metric value per Pod, averaged across Pods.
- `Object`: one metric attached to a Kubernetes object, such as an Ingress or Service.
- `External`: one metric from outside the Kubernetes object model, such as a cloud queue.

## Required Metrics APIs

HPA reads metrics through Kubernetes API aggregation:

```text
metrics.k8s.io           -> resource metrics, usually Metrics Server
custom.metrics.k8s.io    -> custom Kubernetes object or Pod metrics
external.metrics.k8s.io  -> external provider metrics
```

For custom or external metrics, you need an adapter.

Common adapters:

- Prometheus Adapter.
- Datadog Cluster Agent.
- Cloud provider or queue-specific adapters.
- Custom metrics API implementations.

## Apply The Demo App

The demo app exposes:

```text
/       -> increments request counter
/work   -> increments work counter
/metrics -> Prometheus-style metrics
```

From `sessions/12-pod-autoscaling`:

```bash
kubectl apply -f subsessions/01-resource-guardrails/
kubectl apply -f subsessions/07-custom-external-metrics-hpa/01-custom-metric-demo.yml
```

Generate traffic:

```bash
kubectl apply -f subsessions/07-custom-external-metrics-hpa/02-custom-metric-load-generator.yml
```

Check:

```bash
kubectl get pods -n app-scaling-prod -l app=custom-metric-demo
kubectl port-forward -n app-scaling-prod service/custom-metric-demo 8080:80
```

Open:

```text
http://localhost:8080/metrics
```

## Prometheus Adapter Concept

Prometheus scrapes the app's `/metrics` endpoint.

The adapter maps Prometheus queries into Kubernetes custom metrics.

Conceptual adapter rule:

```yaml
rules:
  custom:
    - seriesQuery: 'http_requests_total{namespace!="",pod!=""}'
      resources:
        overrides:
          namespace:
            resource: namespace
          pod:
            resource: pod
      name:
        matches: "^(.*)_total"
        as: "${1}_per_second"
      metricsQuery: 'sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)'
```

This can expose a Pod metric named:

```text
http_requests_per_second
```

The sample HPA in `03-custom-pods-metric-hpa-example.yml` uses that metric.

Apply it only after your custom metrics API exposes the metric:

```bash
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta2" | jq
kubectl apply -f subsessions/07-custom-external-metrics-hpa/03-custom-pods-metric-hpa-example.yml
```

## External Metric Concept

External metrics are not tied to one Kubernetes object.

Examples:

- SQS queue depth.
- Kafka lag.
- CloudWatch metric.
- Payment backlog.

The sample HPA in `04-external-queue-metric-hpa-example.yml` expects an external metric named:

```text
sqs_queue_messages_visible
```

Apply it only after your external metrics adapter exposes that metric:

```bash
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1" | jq
kubectl apply -f subsessions/07-custom-external-metrics-hpa/04-external-queue-metric-hpa-example.yml
```

## Debug

```bash
kubectl describe hpa custom-metric-demo -n app-scaling-prod
kubectl get apiservice | grep metrics
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta2" | jq
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1" | jq
```

Common failures:

- Metrics adapter is not installed.
- Prometheus is not scraping the app.
- Metric names do not match adapter rules.
- Metric labels do not map to `namespace` and `pod`.
- HPA selector does not match the series exposed by the adapter.

## Cleanup

```bash
kubectl delete -f subsessions/07-custom-external-metrics-hpa/04-external-queue-metric-hpa-example.yml --ignore-not-found
kubectl delete -f subsessions/07-custom-external-metrics-hpa/03-custom-pods-metric-hpa-example.yml --ignore-not-found
kubectl delete -f subsessions/07-custom-external-metrics-hpa/02-custom-metric-load-generator.yml --ignore-not-found
kubectl delete -f subsessions/07-custom-external-metrics-hpa/01-custom-metric-demo.yml --ignore-not-found
```

## Review Questions

1. Why might CPU be a poor scaling signal for a queue worker?
2. What does a metrics adapter do?
3. What is the difference between custom and external metrics?
4. Why must metric labels map cleanly to Kubernetes resources?
5. Why does HPA choose the highest recommendation when multiple metrics are configured?
