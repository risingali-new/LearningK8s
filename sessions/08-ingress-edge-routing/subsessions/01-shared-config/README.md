# Sub-Session 01: Shared Config

This sub-session creates the namespace and shared configuration for the ingress lab.

## Objects Created

- Namespace: `app-ingress`
- ConfigMap: `app-config`
- Secret: `app-secrets`

The API microservices use these values to connect to PostgreSQL.

## Apply

From `sessions/08-ingress-edge-routing`:

```bash
kubectl apply -f subsessions/01-shared-config/
```

## Check

```bash
kubectl get namespace app-ingress
kubectl get configmap -n app-ingress
kubectl get secret -n app-ingress
```
