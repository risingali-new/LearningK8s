# Sub-Session 08: Optional Traefik Ingress

This optional sub-session exposes the same frontend and API Services through
Traefik instead of the AWS Load Balancer Controller.

Use this when you want to practice a developer-friendly edge router that can
grow from basic Kubernetes Ingress into middleware, CRDs, and API gateway
patterns.

## Where Traefik Fits

| Area | Detail |
|---|---|
| Best fit | Developer-heavy teams and small to medium platforms that want dynamic routing with simple operations. |
| Strong scenarios | Kubernetes Ingress, Gateway API, Traefik CRDs such as `IngressRoute`, middleware, dashboards, and Let's Encrypt automation. |
| Watch outs | It does not expose AWS ALB-specific features. Platform teams should standardize middleware and security patterns before broad production use. |
| Lab `IngressClass` | `traefik` |

## Prerequisites

Start from the normal Session 08 app state:

```bash
kubectl apply -f subsessions/01-shared-config/
kubectl apply -f subsessions/02-storageclass/
kubectl apply -f subsessions/03-postgres-statefulset/
kubectl apply -f subsessions/04-api-microservices/
kubectl apply -f subsessions/05-frontend/
```

Install Traefik with Kubernetes Ingress provider enabled, then confirm the
class:

```bash
kubectl get ingressclass
```

Expected:

```text
traefik
```

If your installation uses a different class name, update `ingressClassName` in
the manifest before applying it.

## Install Controller With A LoadBalancer

Install with Helm and create a cloud `LoadBalancer` Service for Traefik:

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update

helm install traefik traefik/traefik \
  --namespace traefik \
  --create-namespace \
  --set service.type=LoadBalancer \
  --set providers.kubernetesIngress.enabled=true
```

Check the controller Service and wait for an external hostname:

```bash
kubectl get pods -n traefik
kubectl get service -n traefik traefik
```

Copy the external hostname from the `traefik` `LoadBalancer` Service. That
hostname is the browser entry point for this lab.

## Routing

```text
http://<traefik-load-balancer-dns>/          -> frontend:80
http://<traefik-load-balancer-dns>/api/users -> user-service:5001
http://<traefik-load-balancer-dns>/api/apps  -> app-service:5002
```

This lab uses a standard Kubernetes Ingress so the app shape stays identical to
the ALB example. It intentionally omits the Ingress host so students can open
the Traefik load balancer DNS directly in a browser. Traefik-specific features
such as middlewares can be added after the basic routing works.

## Apply

From `sessions/08-ingress-edge-routing`, remove other Ingress resources first:

```bash
kubectl delete ingress -n app-ingress --all --ignore-not-found
```

Apply the Traefik Ingress:

```bash
kubectl apply -f subsessions/08-optional-traefik-ingress/
```

## Check

```bash
kubectl get ingress -n app-ingress
kubectl describe ingress message-board-ingress-traefik -n app-ingress
```

Wait for an address:

```bash
kubectl get ingress message-board-ingress-traefik -n app-ingress -w
```

## Test

```bash
export APP_DNS=<traefik-ingress-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/messages
curl http://$APP_DNS/api/apps/stats
```

Open the load balancer DNS in a browser:

```text
http://<traefik-load-balancer-dns>
```

## Cleanup

```bash
kubectl delete -f subsessions/08-optional-traefik-ingress/ --ignore-not-found
```

This removes only the lab Ingress. It does not uninstall Traefik.

Reference:

```text
https://doc.traefik.io/traefik/reference/install-configuration/providers/kubernetes/kubernetes-ingress/
```
