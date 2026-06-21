# Sub-Session 09: Optional HAProxy Ingress

This optional sub-session exposes the same frontend and API Services through
HAProxy Ingress instead of the AWS Load Balancer Controller.

Use this when you want to practice a Kubernetes Ingress controller backed by
HAProxy load-balancing behavior.

## Where HAProxy Fits

| Area | Detail |
|---|---|
| Best fit | Teams that already use HAProxy and want familiar load-balancer behavior inside Kubernetes. |
| Strong scenarios | HTTP routing, TCP routing, SSL/TLS, header manipulation, rate limiting, and predictable edge tuning. |
| Watch outs | It is not AWS-native ALB provisioning, and Gateway API support may come through different HAProxy products or installation paths. |
| Lab `IngressClass` | `haproxy` |

## Prerequisites

Start from the normal Session 03 app state:

```bash
kubectl apply -f subsessions/01-shared-config/
kubectl apply -f subsessions/02-storageclass/
kubectl apply -f subsessions/03-postgres-statefulset/
kubectl apply -f subsessions/04-api-microservices/
kubectl apply -f subsessions/05-frontend/
```

Install HAProxy Ingress, then confirm the class:

```bash
kubectl get ingressclass
```

Expected:

```text
haproxy
```

If your installation uses a different class name, update `ingressClassName` in
the manifest before applying it.

## Install Controller With A LoadBalancer

Install with Helm and create a cloud `LoadBalancer` Service for HAProxy:

```bash
helm repo add haproxytech https://haproxytech.github.io/helm-charts
helm repo update

helm install haproxy-kubernetes-ingress haproxytech/kubernetes-ingress \
  --namespace haproxy-controller \
  --create-namespace \
  --set controller.service.type=LoadBalancer
```

Check the controller Service and wait for an external hostname:

```bash
kubectl get pods -n haproxy-controller
kubectl get service -n haproxy-controller
```

Copy the external hostname from the HAProxy `LoadBalancer` Service. That
hostname is the browser entry point for this lab.

## Routing

```text
http://<haproxy-load-balancer-dns>/          -> frontend:80
http://<haproxy-load-balancer-dns>/api/users -> user-service:5001
http://<haproxy-load-balancer-dns>/api/apps  -> app-service:5002
```

This lab uses standard Ingress paths and intentionally omits the Ingress host so
students can open the HAProxy load balancer DNS directly in a browser. After
the basic route works, HAProxy annotations can be added for controller-specific
behavior.

## Apply

From `sessions/03-ingress`, remove other Ingress resources first:

```bash
kubectl delete ingress -n app-ingress --all --ignore-not-found
```

Apply the HAProxy Ingress:

```bash
kubectl apply -f subsessions/09-optional-haproxy-ingress/
```

## Check

```bash
kubectl get ingress -n app-ingress
kubectl describe ingress message-board-ingress-haproxy -n app-ingress
```

Wait for an address:

```bash
kubectl get ingress message-board-ingress-haproxy -n app-ingress -w
```

## Test

```bash
export APP_DNS=<haproxy-ingress-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/messages
curl http://$APP_DNS/api/apps/stats
```

Open the load balancer DNS in a browser:

```text
http://<haproxy-load-balancer-dns>
```

## Cleanup

```bash
kubectl delete -f subsessions/09-optional-haproxy-ingress/ --ignore-not-found
```

This removes only the lab Ingress. It does not uninstall HAProxy Ingress.

Reference:

```text
https://www.haproxy.com/documentation/kubernetes-ingress/overview/
```
