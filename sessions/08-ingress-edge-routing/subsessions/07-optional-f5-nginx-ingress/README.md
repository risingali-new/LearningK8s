# Sub-Session 07: Optional F5 NGINX Ingress Controller

This optional sub-session exposes the same frontend and API Services through
F5 NGINX Ingress Controller instead of the AWS Load Balancer Controller.

Use this when you want to practice a commercial NGINX-based Ingress controller
with standard Kubernetes Ingress resources.

## Where F5 NGINX Fits

| Area | Detail |
|---|---|
| Best fit | Teams that already use NGINX or want F5/NGINX commercial support. |
| Strong scenarios | Standard HTTP routing, TLS termination, NGINX annotations, NGINX Plus features, and enterprise operations. |
| Watch outs | It does not create AWS ALB resources from Ingress like the AWS Load Balancer Controller. It is also not a service mesh by itself. |
| Lab `IngressClass` | `nginx` |

## Prerequisites

Start from the normal Session 08 app state:

```bash
kubectl apply -f subsessions/01-shared-config/
kubectl apply -f subsessions/02-storageclass/
kubectl apply -f subsessions/03-postgres-statefulset/
kubectl apply -f subsessions/04-api-microservices/
kubectl apply -f subsessions/05-frontend/
```

Install F5 NGINX Ingress Controller, then confirm the class:

```bash
kubectl get ingressclass
```

Expected:

```text
nginx
```

If your controller uses a different class name, update `ingressClassName` in the
manifest before applying it.

## Install Controller With A LoadBalancer

Install with Helm and create a cloud `LoadBalancer` Service for the controller:

```bash
helm install f5-nginx-ingress oci://ghcr.io/nginx/charts/nginx-ingress \
  --version 2.6.1 \
  --namespace nginx-ingress \
  --create-namespace \
  --set controller.service.type=LoadBalancer \
  --set controller.allowEmptyIngressHost=true
```

Check the controller Service and wait for an external hostname:

```bash
kubectl get pods -n nginx-ingress
kubectl get service -n nginx-ingress
```

Copy the external hostname from the `LoadBalancer` Service. That hostname is the
browser entry point for this lab.

## Routing

```text
http://<nginx-load-balancer-dns>/          -> frontend:80
http://<nginx-load-balancer-dns>/api/users -> user-service:5001
http://<nginx-load-balancer-dns>/api/apps  -> app-service:5002
```

This lab intentionally omits the Ingress host so students can open the
controller load balancer DNS directly in a browser.

## Apply

From `sessions/08-ingress-edge-routing`, remove other Ingress resources first:

```bash
kubectl delete ingress -n app-ingress --all --ignore-not-found
```

Apply the F5 NGINX Ingress:

```bash
kubectl apply -f subsessions/07-optional-f5-nginx-ingress/
```

## Check

```bash
kubectl get ingress -n app-ingress
kubectl describe ingress message-board-ingress-f5-nginx -n app-ingress
```

Wait for an address:

```bash
kubectl get ingress message-board-ingress-f5-nginx -n app-ingress -w
```

## Test

```bash
export APP_DNS=<nginx-ingress-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/messages
curl http://$APP_DNS/api/apps/stats
```

Open the load balancer DNS in a browser:

```text
http://<nginx-load-balancer-dns>
```

## Cleanup

```bash
kubectl delete -f subsessions/07-optional-f5-nginx-ingress/ --ignore-not-found
```

This removes only the lab Ingress. It does not uninstall F5 NGINX Ingress
Controller.

Reference:

```text
https://docs.nginx.com/nginx-ingress-controller/
```
