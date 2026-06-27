# Sub-Session 06: Flask Services

This sub-session exposes the Flask Deployment with Kubernetes Services.

## Why Service Is Used

Pods are temporary and their IP addresses change. A Service provides a stable virtual IP and DNS name for a group of Pods.

Services route traffic to Pods using label selectors.

## How Kubernetes Uses It

The Flask Pods have labels:

```yaml
app: flask-web
tier: application
```

The Service selector uses the same labels:

```yaml
selector:
  app: flask-web
  tier: application
```

If the selector does not match the Pod labels, the Service has no endpoints.

## Service Types In This Sub-Session

### ClusterIP

Internal-only service. Use this when traffic comes from inside the cluster.

Manifest:

```text
01-flask-service-clusterip.yml
```

### NodePort

Exposes the service on a port on every node.

Manifest:

```text
02-flask-service-nodeport.yml
```

### LoadBalancer

Asks the cloud provider for an external load balancer.

Manifest:

```text
03-flask-service-loadbalancer.yml
```

On EKS, this is the common beginner-friendly way to expose the app publicly.

## Apply ClusterIP

From `sessions/02-core-k8s`:

```bash
kubectl apply -f subsessions/06-flask-services/01-flask-service-clusterip.yml
```

Access with port-forward:

```bash
kubectl port-forward -n app-core service/flask-web-clusterip 8080:80
```

Open:

```text
http://localhost:8080
```

## Apply NodePort

```bash
kubectl apply -f subsessions/06-flask-services/02-flask-service-nodeport.yml
kubectl get service flask-web-nodeport -n app-core
```

## Apply LoadBalancer

```bash
kubectl apply -f subsessions/06-flask-services/03-flask-service-loadbalancer.yml
kubectl get service flask-web-loadbalancer -n app-core
```

Wait for `EXTERNAL-IP` on a cloud cluster.

## Check Endpoints

```bash
kubectl get endpoints -n app-core
```

If the Flask service has no endpoints, check Deployment Pod labels and Service selectors.

