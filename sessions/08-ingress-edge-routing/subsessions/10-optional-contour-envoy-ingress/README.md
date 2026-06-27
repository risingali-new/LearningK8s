# Sub-Session 10: Optional Contour / Envoy Ingress

This optional sub-session exposes the same frontend and API Services through
Contour and Envoy instead of the AWS Load Balancer Controller.

Use this when you want to practice Envoy-based ingress without adopting a full
service mesh.

## Where Contour / Envoy Fits

| Area | Detail |
|---|---|
| Best fit | Platform teams that want Envoy at the edge with a lightweight Kubernetes control plane. |
| Strong scenarios | Standard Ingress, Contour `HTTPProxy`, Gateway API, gRPC, Envoy metrics, and multi-team route ownership. |
| Watch outs | It adds Envoy operating knowledge. If you need mesh-wide policy and telemetry, Istio may be the better fit. |
| Lab `IngressClass` | `contour` |

## Prerequisites

Start from the normal Session 08 app state:

```bash
kubectl apply -f subsessions/01-shared-config/
kubectl apply -f subsessions/02-storageclass/
kubectl apply -f subsessions/03-postgres-statefulset/
kubectl apply -f subsessions/04-api-microservices/
kubectl apply -f subsessions/05-frontend/
```

Install Contour, then confirm the class:

```bash
kubectl get ingressclass
```

Expected:

```text
contour
```

Contour can be configured with a different IngressClass name. If your cluster
uses a different value, update `ingressClassName` before applying the manifest.

## Install Controller With A LoadBalancer

Install with Helm. Contour uses Envoy as the data plane, and Envoy is the
component exposed through the cloud `LoadBalancer` Service:

```bash
helm repo add contour https://projectcontour.github.io/helm-charts/
helm repo update

helm install contour contour/contour \
  --namespace projectcontour \
  --create-namespace
```

Check the Contour and Envoy Pods, then wait for the Envoy Service to receive an
external hostname:

```bash
kubectl get pods -n projectcontour
kubectl get service -n projectcontour
```

Copy the external hostname from the Envoy `LoadBalancer` Service. That hostname
is the browser entry point for this lab.

## Routing

```text
http://<envoy-load-balancer-dns>/          -> frontend:80
http://<envoy-load-balancer-dns>/api/users -> user-service:5001
http://<envoy-load-balancer-dns>/api/apps  -> app-service:5002
```

This lab uses standard Kubernetes Ingress. Contour-specific `HTTPProxy` and
Gateway API resources are useful follow-up exercises after this route works.
The manifest intentionally omits the Ingress host so students can open the
Envoy load balancer DNS directly in a browser.

## Apply

From `sessions/08-ingress-edge-routing`, remove other Ingress resources first:

```bash
kubectl delete ingress -n app-ingress --all --ignore-not-found
```

Apply the Contour Ingress:

```bash
kubectl apply -f subsessions/10-optional-contour-envoy-ingress/
```

## Check

```bash
kubectl get ingress -n app-ingress
kubectl describe ingress message-board-ingress-contour -n app-ingress
```

Wait for an address:

```bash
kubectl get ingress message-board-ingress-contour -n app-ingress -w
```

## Test

```bash
export APP_DNS=<contour-envoy-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/messages
curl http://$APP_DNS/api/apps/stats
```

Open the load balancer DNS in a browser:

```text
http://<envoy-load-balancer-dns>
```

## Cleanup

```bash
kubectl delete -f subsessions/10-optional-contour-envoy-ingress/ --ignore-not-found
```

This removes only the lab Ingress. It does not uninstall Contour or Envoy.

Reference:

```text
https://projectcontour.io/docs/main/
```
