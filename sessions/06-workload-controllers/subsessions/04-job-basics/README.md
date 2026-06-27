# Sub-Session 04: Job Basics

This sub-session introduces Kubernetes Jobs for finite work.

## Concepts

```text
Job
  -> creates Pods
    -> retries failed Pods
      -> finishes when completions succeed
```

Use Jobs for tasks such as migrations, reports, image processing, and one-time
batch work.

## Apply

From `sessions/06-workload-controllers`:

```bash
kubectl apply -f subsessions/04-job-basics/
```

## Check

```bash
kubectl get jobs -n daemonset-lab
kubectl get pods -n daemonset-lab -l job-name=batch-hello
kubectl logs -n daemonset-lab job/batch-hello
kubectl describe job batch-hello -n daemonset-lab
```

## Cleanup

```bash
kubectl delete -f subsessions/04-job-basics/ --ignore-not-found
```

## Review Questions

1. How is a Job different from a Deployment?
2. What does `backoffLimit` control?
3. When would you use `completions` and `parallelism`?
