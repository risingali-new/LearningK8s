# Sub-Session 12: Optional Cilium Ingress

This optional sub-session exposes the same frontend and API Services through
Cilium Ingress instead of the AWS Load Balancer Controller.

Use this when the cluster already uses Cilium and you want ingress integrated
with Cilium networking, Envoy, and policy.

## Where Cilium Fits

| Area | Detail |
|---|---|
| Best fit | Clusters already using Cilium as the CNI. |
| Strong scenarios | eBPF networking, Cilium NetworkPolicy around ingress, Envoy per-node proxying, Gateway API, and source IP visibility. |
| Watch outs | Cilium Ingress is tied closely to the CNI. If the cluster does not use Cilium, choose a standalone controller instead. |
| Lab `IngressClass` | `cilium` |

## Prerequisites

Start from the normal Session 03 app state:

```bash
kubectl apply -f subsessions/01-shared-config/
kubectl apply -f subsessions/02-storageclass/
kubectl apply -f subsessions/03-postgres-statefulset/
kubectl apply -f subsessions/04-api-microservices/
kubectl apply -f subsessions/05-frontend/
```

Cilium must be installed with ingress support enabled. Confirm the class:

```bash
kubectl get ingressclass
```

Expected:

```text
cilium
```

Cilium Ingress normally creates a `LoadBalancer` Service for the Ingress. Your
environment must support `LoadBalancer` Services, or Cilium must be configured
for another supported exposure mode such as NodePort or host network mode.

## Install Or Enable Controller With A LoadBalancer

Use this path only on a cluster intended to run Cilium. If the cluster already
uses a different CNI, do not replace it during a shared class lab unless that is
the planned exercise.

For a fresh Cilium lab cluster, install Cilium with the Ingress controller
enabled and a dedicated `LoadBalancer` per Ingress:

```bash
cilium install \
  --set ingressController.enabled=true \
  --set ingressController.loadbalancerMode=dedicated
```

If Cilium is already installed with Helm, enable ingress on the existing
release:

```bash
helm repo add cilium https://helm.cilium.io/
helm repo update

helm upgrade cilium cilium/cilium \
  --namespace kube-system \
  --reuse-values \
  --set ingressController.enabled=true \
  --set ingressController.loadbalancerMode=dedicated
```

Check Cilium status:

```bash
cilium status
kubectl get pods -n kube-system -l k8s-app=cilium
```

After you apply this lab Ingress, Cilium creates the Ingress `LoadBalancer`
Service in the application namespace:

```bash
kubectl get service -n app-ingress
```

Copy the external hostname from the Cilium Ingress `LoadBalancer` Service. That
hostname is the browser entry point for this lab.

## Routing

```text
http://<cilium-ingress-load-balancer-dns>/          -> frontend:80
http://<cilium-ingress-load-balancer-dns>/api/users -> user-service:5001
http://<cilium-ingress-load-balancer-dns>/api/apps  -> app-service:5002
```

This lab uses standard Kubernetes Ingress with `ingressClassName: cilium`.
Cilium then programs Envoy through its networking stack. The manifest
intentionally omits the Ingress host so students can open the Cilium-created
load balancer DNS directly in a browser.

## Apply

From `sessions/03-ingress`, remove other Ingress resources first:

```bash
kubectl delete ingress -n app-ingress --all --ignore-not-found
```

Apply the Cilium Ingress:

```bash
kubectl apply -f subsessions/12-optional-cilium-ingress/
```

## Check

```bash
kubectl get ingress -n app-ingress
kubectl describe ingress message-board-ingress-cilium -n app-ingress
```

Wait for an address:

```bash
kubectl get ingress message-board-ingress-cilium -n app-ingress -w
```

You can also inspect Cilium status if the Cilium CLI is available:

```bash
cilium status
```

## Test

```bash
export APP_DNS=<cilium-ingress-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/messages
curl http://$APP_DNS/api/apps/stats
```

Open the load balancer DNS in a browser:

```text
http://<cilium-ingress-load-balancer-dns>
```

## Cleanup

```bash
kubectl delete -f subsessions/12-optional-cilium-ingress/ --ignore-not-found
```

This removes only the lab Ingress. It does not uninstall Cilium.

Reference:

```text
https://docs.cilium.io/en/stable/network/servicemesh/ingress/
```
