# Session 19: Observability

This session teaches how to see what the cluster and applications are doing.

## Sub-Session Order

1. `01-observability-model`: metrics, logs, traces, events.
2. `02-metrics-server`: resource metrics for `kubectl top` and autoscaling.
3. `03-prometheus`: scraping app and cluster metrics.
4. `04-grafana`: dashboards.
5. `05-alertmanager`: alert routing.
6. `06-loki`: centralized logs.
7. `07-opentelemetry`: traces and application telemetry.
8. `08-slo-and-alert-design`: useful alerts versus noise.

## Useful Commands

```bash
kubectl top nodes
kubectl top pods -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl logs -n <namespace> <pod-name>
```

## Review Questions

1. What is the difference between metrics, logs, and traces?
2. Why is Metrics Server not a full monitoring system?
3. What does Prometheus scrape?
4. What makes an alert actionable?
