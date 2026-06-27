# Sub-Session 05: Flask Deployment

This sub-session replaces the standalone Flask Pod with a Deployment.

## Why Deployment Is Used

A Deployment manages stateless application Pods. It keeps the desired number of replicas running and supports rolling updates.

For the Flask tier, a Deployment is the right controller because:

- Flask is stateless.
- Any replica can handle requests.
- Pods can be replaced safely.
- The app can be scaled horizontally.

## How Kubernetes Uses It

The Deployment creates Pods using a Pod template.

It matches its Pods with this selector:

```yaml
matchLabels:
  app: flask-web
  tier: application
```

The template gives new Pods the same labels:

```yaml
labels:
  app: flask-web
  tier: application
```

Selectors and labels must match.

## Manifest

```text
01-flask-deployment.yml
```

## Apply

Delete the standalone Pod first if it still exists:

```bash
kubectl delete pod flask-pod -n app-core --ignore-not-found
```

From `sessions/02-core-k8s`:

```bash
kubectl apply -f subsessions/05-flask-deployment/
```

## Check

```bash
kubectl get deployment flask-web -n app-core
kubectl get pods -n app-core -l app=flask-web
kubectl rollout status deployment/flask-web -n app-core
```

## Scale

```bash
kubectl scale deployment flask-web -n app-core --replicas=3
kubectl get pods -n app-core -l app=flask-web
```

## Self-Healing Test

```bash
kubectl delete pod -n app-core -l app=flask-web
kubectl get pods -n app-core -w
```

The Deployment creates replacement Pods.

