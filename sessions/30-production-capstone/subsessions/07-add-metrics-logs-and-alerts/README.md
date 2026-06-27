# Sub-Session 07: Add Metrics, Logs, And Alerts

This sub-session adds starter observability objects for the capstone app.

## Goal

Expose the frontend to Prometheus discovery and add an alert for missing
frontend replicas.

## App-Based Lab

Install Prometheus Operator first. The app images expose `/metrics` in the
Prometheus text format, so the ServiceMonitor can scrape the frontend Service.

```bash
kubectl apply -f subsessions/07-add-metrics-logs-and-alerts/
```

## Check

```bash
kubectl get servicemonitor,prometheusrule -n message-board-prod
kubectl describe prometheusrule -n message-board-prod message-board-alerts
```

## Cleanup

```bash
kubectl delete -f subsessions/07-add-metrics-logs-and-alerts/ --ignore-not-found
```

## Review Prompts

1. What does Prometheus need in order to discover a Service?
2. Which alert would catch a total frontend outage?
3. What log query would prove an API dependency is failing?
