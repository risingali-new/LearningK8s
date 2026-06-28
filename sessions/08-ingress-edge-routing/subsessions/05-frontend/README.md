# Sub-Session 05: Frontend

This sub-session deploys the browser frontend as its own internal Service.
The frontend image is built from its own folder and Dockerfile:

```text
../../../../app/frontend -> prashantdey/appk8stutorial:frontend-svc-2.0
```

## How It Talks To APIs

The frontend runs `frontend.py` on port `5000` and uses Kubernetes Service DNS to call the APIs:

```text
http://user-service:5001/api/users
http://app-service:5002/api/apps
```

Users do not need those internal names. Users access the app through the Ingress address in the next sub-session.

## Apply

From `sessions/08-ingress-edge-routing`:

```bash
kubectl apply -f subsessions/05-frontend/
```

## Check

```bash
kubectl get deployment frontend -n app-ingress
kubectl get pods -n app-ingress -l app=frontend
kubectl get service frontend -n app-ingress
```

## Internal Test

```bash
kubectl port-forward -n app-ingress service/frontend 8080:80
```

Open:

```text
http://localhost:8080
```
