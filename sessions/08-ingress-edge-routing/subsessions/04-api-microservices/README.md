# Sub-Session 04: API Microservices

This sub-session deploys two internal API services as separate Flask processes.
Each API service is built from its own folder and Dockerfile:

```text
../../../../app/user-service  -> prashantdey/appk8stutorial:user-svc-2.0
../../../../app/app-service   -> prashantdey/appk8stutorial:app-svc-2.0
```

## Services

`user-service` runs `user_service.py` on port `5001` and handles users:

```text
GET  /api/users
POST /api/users
GET  /api/users/stats
```

`app-service` runs `app_service.py` on port `5002` and handles application messages:

```text
GET    /api/apps
GET    /api/apps/messages
POST   /api/apps/messages
DELETE /api/apps/messages/<id>
GET    /api/apps/stats
```

Both Services are `ClusterIP`. They are internal until the Ingress routes traffic to them.

## Apply

From `sessions/08-ingress-edge-routing`:

```bash
kubectl apply -f subsessions/04-api-microservices/
```

## Check

```bash
kubectl get deployment -n app-ingress
kubectl get service -n app-ingress
kubectl get endpoints -n app-ingress
```

## Internal Test

```bash
kubectl port-forward -n app-ingress service/user-service 8081:5001
curl http://localhost:8081/api/users
```

In another terminal:

```bash
kubectl port-forward -n app-ingress service/app-service 8082:5002
curl http://localhost:8082/api/apps
```
