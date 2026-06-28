# Sub-Session 01: Version Skew

This sub-session is part of 28-cluster-operations.

## Goal

Kubernetes component compatibility.

## App-Based Lab

Use the existing training application as the example workload. The app is the same Flask/PostgreSQL or frontend/API service set used across this repository, so the Kubernetes concept is always shown against a real workload.

If this folder contains YAML, apply it from the session root:

```bash
kubectl apply -f subsessions/01-version-skew/
```

## Check

```bash
kubectl get all -A
kubectl get events -A --sort-by=.lastTimestamp
```

## Cleanup

```bash
kubectl delete -f subsessions/01-version-skew/ --ignore-not-found
```

## Review Prompts

1. Which part of the training app is affected by this concept?
2. Which Kubernetes object owns the desired state?
3. What command proves the expected behavior?
