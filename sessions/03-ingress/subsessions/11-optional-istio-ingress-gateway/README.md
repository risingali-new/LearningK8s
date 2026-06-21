# Sub-Session 11: Optional Istio Ingress Gateway

This optional sub-session exposes the same frontend and API Services through
Istio's ingress handling instead of the AWS Load Balancer Controller.

Use this when you want to see how the same app can enter a cluster that already
uses Istio. This parity lab uses a standard Kubernetes `Ingress`; real Istio
traffic management usually uses Istio `Gateway` and `VirtualService`, or the
Kubernetes Gateway API.

## Where Istio Fits

| Area | Detail |
|---|---|
| Best fit | Clusters already using Istio or teams that need ingress tied to service mesh policy. |
| Strong scenarios | mTLS, traffic shifting, retries, timeouts, circuit breaking, authorization policy, telemetry, and mesh-aware routing. |
| Watch outs | It is heavier than a simple Ingress controller. If you only need basic HTTP routing, ALB, NGINX, Traefik, HAProxy, or Contour may be simpler. |
| Lab `IngressClass` | `istio` |

## Prerequisites

Start from the normal Session 03 app state:

```bash
kubectl apply -f subsessions/01-shared-config/
kubectl apply -f subsessions/02-storageclass/
kubectl apply -f subsessions/03-postgres-statefulset/
kubectl apply -f subsessions/04-api-microservices/
kubectl apply -f subsessions/05-frontend/
```

Install Istio and ensure an ingress gateway is available. This lab creates an
`IngressClass` named `istio` that points to the Istio ingress controller:

```text
controller: istio.io/ingress-controller
```

If your Istio setup already creates this IngressClass, applying the file should
be harmless if it matches. If your cluster uses a different convention, review
the file before applying it.

## Install Controller With A LoadBalancer

Install Istio with Helm, then install an ingress gateway exposed through a cloud
`LoadBalancer` Service:

```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

helm install istio-base istio/base \
  --namespace istio-system \
  --create-namespace

helm install istiod istio/istiod \
  --namespace istio-system \
  --wait

helm install istio-ingressgateway istio/gateway \
  --namespace istio-ingress \
  --create-namespace \
  --set service.type=LoadBalancer \
  --wait
```

Check the gateway Service and wait for an external hostname:

```bash
kubectl get pods -n istio-system
kubectl get pods -n istio-ingress
kubectl get service -n istio-ingress
```

Copy the external hostname from the Istio gateway `LoadBalancer` Service. That
hostname is the browser entry point for this lab.

## Routing

```text
http://<istio-gateway-load-balancer-dns>/          -> frontend:80
http://<istio-gateway-load-balancer-dns>/api/users -> user-service:5001
http://<istio-gateway-load-balancer-dns>/api/apps  -> app-service:5002
```

This lab intentionally omits the Ingress host so students can open the Istio
gateway load balancer DNS directly in a browser.

## Apply

From `sessions/03-ingress`, remove other Ingress resources first:

```bash
kubectl delete ingress -n app-ingress --all --ignore-not-found
```

Apply the Istio IngressClass and Ingress:

```bash
kubectl apply -f subsessions/11-optional-istio-ingress-gateway/
```

## Check

```bash
kubectl get ingressclass istio
kubectl get ingress -n app-ingress
kubectl describe ingress message-board-ingress-istio -n app-ingress
```

Wait for an address:

```bash
kubectl get ingress message-board-ingress-istio -n app-ingress -w
```

If the Ingress address is empty, use the gateway Service address:

```bash
kubectl get service -n istio-ingress
```

## Test

```bash
export APP_DNS=<istio-ingress-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/messages
curl http://$APP_DNS/api/apps/stats
```

Open the load balancer DNS in a browser:

```text
http://<istio-gateway-load-balancer-dns>
```

## Cleanup

```bash
kubectl delete -f subsessions/11-optional-istio-ingress-gateway/ --ignore-not-found
```

This removes the lab Ingress and lab IngressClass. It does not uninstall Istio.

Reference:

```text
https://istio.io/latest/docs/tasks/traffic-management/ingress/kubernetes-ingress/
```
