# Sub-Session 03: PostgreSQL Deployment And Service

This sub-session starts the database tier with ephemeral storage and exposes it internally with a Service.

## Why Deployment Is Used For PostgreSQL In This Session

In a later storage session, PostgreSQL will run as a StatefulSet. Here, the goal is simpler: teach Deployments and Services before introducing persistent storage.

The PostgreSQL Deployment:

- Runs one PostgreSQL Pod.
- Restarts the Pod if it fails.
- Reads credentials from the Secret.
- Uses `emptyDir` storage for now.

Important: `emptyDir` is temporary. Data can be lost when the Pod is replaced.

## Why Service Is Used

Pods have changing IP addresses. The Flask app needs a stable way to reach PostgreSQL.

The PostgreSQL Service gives this stable DNS name:

```text
postgres.app-core.svc.cluster.local
```

Inside the same namespace, Flask can simply use:

```text
postgres
```

## How Kubernetes Uses It

The Service selector matches PostgreSQL Pod labels:

```yaml
selector:
  app: postgres
  tier: data
```

If labels and selectors do not match, the Service has no endpoints.

## Manifests

```text
01-postgres-deployment.yml
02-postgres-service.yml
```

## Apply

Run the previous sub-sessions first.

From `sessions/02-core-k8s`:

```bash
kubectl apply -f subsessions/03-postgres-deployment-service/
```

## Check

```bash
kubectl get deployment -n app-core
kubectl get pods -n app-core -l app=postgres
kubectl get service postgres -n app-core
kubectl get endpoints postgres -n app-core
```

## Troubleshoot

```bash
kubectl describe pod -n app-core -l app=postgres
kubectl logs -n app-core deployment/postgres
```

