# Sub-Session 03: PostgreSQL StatefulSet

This sub-session creates the database layer for the microservices app.

## Why This Comes First

Both API microservices use PostgreSQL:

- `user-service` reads and writes user records.
- `app-service` reads and writes message records.

## Apply

From `sessions/08-ingress-edge-routing`:

```bash
kubectl apply -f subsessions/03-postgres-statefulset/
```

## Check

```bash
kubectl get statefulset -n app-ingress
kubectl get pods -n app-ingress -l app=postgres,session=ingress
kubectl get pvc -n app-ingress
```
