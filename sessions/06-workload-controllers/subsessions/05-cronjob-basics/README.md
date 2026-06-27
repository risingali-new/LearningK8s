# Sub-Session 05: CronJob Basics

This sub-session introduces Kubernetes CronJobs for scheduled Jobs.

## Concepts

```text
CronJob schedule
  -> creates Job
    -> Job creates Pod
      -> Pod runs to completion
```

Use CronJobs for reports, cleanup tasks, sync jobs, and periodic checks.

## Apply

From `sessions/06-workload-controllers`:

```bash
kubectl apply -f subsessions/05-cronjob-basics/
```

## Check

```bash
kubectl get cronjobs -n daemonset-lab
kubectl get jobs -n daemonset-lab
kubectl get pods -n daemonset-lab
```

Wait for the next minute boundary, then inspect the created Job:

```bash
kubectl logs -n daemonset-lab -l app=cron-hello
```

## Cleanup

```bash
kubectl delete -f subsessions/05-cronjob-basics/ --ignore-not-found
```

## Review Questions

1. What object does a CronJob create?
2. What does `concurrencyPolicy` control?
3. Why should successful and failed job history limits be configured?
