# Sub-Session 04: Flask As A Standalone Pod

This sub-session runs the Flask app as a single Pod so students can understand the smallest deployable Kubernetes workload.

## Why Pod Is Used

A Pod is the smallest deployable unit in Kubernetes. It wraps one or more containers and gives them:

- A shared network namespace.
- A Pod IP.
- Shared volumes when configured.

Production apps are usually not managed as standalone Pods, but learning Pods directly makes Deployments easier to understand.

## How Kubernetes Uses It

The Flask Pod:

- Runs image `prashantdey/appk8stutorial:1.0`.
- Reads database configuration from ConfigMap and Secret.
- Connects to PostgreSQL through the `postgres` Service.
- Exposes container port `5000`.

## Manifest

```text
01-flask-pod.yml
```

## Apply

Run sub-sessions 01, 02, and 03 first.

From `sessions/02-core-k8s`:

```bash
kubectl apply -f subsessions/04-flask-pod/
```

## Check

```bash
kubectl get pod flask-pod -n app-core
kubectl describe pod flask-pod -n app-core
kubectl logs flask-pod -n app-core
```

## Access

```bash
kubectl port-forward -n app-core pod/flask-pod 8080:5000
```

Open:

```text
http://localhost:8080
```

## Important Experiment

Delete the standalone Pod:

```bash
kubectl delete pod flask-pod -n app-core
kubectl get pods -n app-core
```

It does not come back automatically. That is why the next sub-session replaces it with a Deployment.

