# Sub-Session 04: Flask With Persistent PostgreSQL

This sub-session deploys the Flask app and connects it to the PostgreSQL database that is using persistent storage.

## Why Flask Still Uses Deployment

Flask is stateless. It does not store the submitted messages in its local filesystem. It sends them to PostgreSQL.

That means Flask can safely run as a Deployment with multiple replicas.

## How Kubernetes Connects Flask To PostgreSQL

The Flask container receives:

```text
DB_HOST=postgres
DB_PORT=5432
```

`postgres` is the Kubernetes Service name for the database.

## Manifests

```text
01-flask-deployment.yml
02-flask-service.yml
```

The Service is a `LoadBalancer` so the app can be exposed on a cloud cluster. For local clusters, use port forwarding.

## Apply

Run either the static PostgreSQL sub-session or the StatefulSet sub-session first.

From `sessions/07-storage-pv-pvc-statefulset`:

```bash
kubectl apply -f subsessions/04-flask-with-persistent-db/
```

## Check

```bash
kubectl get deployment flask-web -n app-storage
kubectl get pods -n app-storage -l app=flask-web
kubectl get service flask-web -n app-storage
```

## Access

Local access:

```bash
kubectl port-forward -n app-storage service/flask-web 8080:80
```

Open:

```text
http://localhost:8080
```

Cloud access:

```bash
kubectl get service flask-web -n app-storage
```

Use the `EXTERNAL-IP` when it is available.

## PostgreSQL Pod Restart Behavior

After messages are saved through Flask, you can delete the PostgreSQL Pod to prove that the data is not stored inside the container filesystem:

```bash
kubectl delete pod -n app-storage -l app=postgres,storage-demo=static
kubectl get pods -n app-storage -w
```

While the replacement PostgreSQL Pod is starting, Flask may temporarily show:

```text
Database is not available yet.
```

This is expected during the restart window. The `postgres` Service only sends traffic to ready PostgreSQL Pods. When the old Pod is deleted and the new Pod is not ready yet, there may be no ready database endpoint for Flask to use.

Wait for PostgreSQL to become ready:

```bash
kubectl wait -n app-storage --for=condition=ready pod -l app=postgres,storage-demo=static --timeout=180s
kubectl get endpoints postgres -n app-storage
```

Then refresh the Flask page. The messages should be visible again.

## If The Database Stays Unavailable

Check the PostgreSQL Pod, PVC, Service endpoints, and Flask Deployment:

```bash
kubectl get pods -n app-storage
kubectl get pvc -n app-storage
kubectl describe pvc postgres-data-static -n app-storage
kubectl get endpoints postgres -n app-storage
kubectl logs -n app-storage deployment/postgres
kubectl logs -n app-storage deployment/flask-web
```

Common causes:

- The PVC is not `Bound`.
- The PostgreSQL Pod is not `Ready`.
- The `postgres` Service has no endpoints.
- PostgreSQL is still initializing the data directory.
- On a multi-node cluster, the static `hostPath` volume may point to a path on a different node after the Pod is recreated.

For the static `hostPath` lab, the safest demo environment is a single-node local cluster such as minikube, kind, or Docker Desktop. In a multi-node cluster, `hostPath` is node-local storage. If PostgreSQL is recreated on another node, Kubernetes may create or use an empty path on that node, so the previous data will not be available.

## Fix Options

Use these fixes depending on what failed.

1. If PostgreSQL is still starting, wait for the Pod to become ready and refresh the Flask page:

```bash
kubectl wait -n app-storage --for=condition=ready pod -l app=postgres,storage-demo=static --timeout=180s
```

2. If Flask Pods are unhealthy because they started while PostgreSQL was unavailable, restart Flask after PostgreSQL is ready:

```bash
kubectl rollout restart deployment/flask-web -n app-storage
kubectl rollout status deployment/flask-web -n app-storage
```

3. If the PVC is not bound, recreate the static PV and PVC in the correct order:

```bash
kubectl apply -f subsessions/02-static-pv-pvc/
kubectl get pv
kubectl get pvc -n app-storage
```

4. If the lab is running on a multi-node cloud cluster, move to the dynamic storage flow from the next sub-sessions:

```bash
kubectl delete -f subsessions/03-postgres-with-static-pvc/ --ignore-not-found
kubectl apply -f subsessions/05-storageclass/
kubectl apply -f subsessions/06-postgres-statefulset/
```

The dynamic flow uses a StorageClass and StatefulSet `volumeClaimTemplates`, so Kubernetes creates the PVC and PV through the CSI driver instead of relying on a node-local `hostPath`.
