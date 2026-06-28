# Session 08: Ingress And Edge Routing With Multiple Microservices

This session refactors the app deployment shape from one Flask service into separate microservices behind one Ingress.

It reuses the PostgreSQL StatefulSet pattern from Session 07. The new idea in this session is external HTTP routing to multiple internal Services.

The default path uses the AWS Load Balancer Controller and an ALB-backed
Ingress. Optional controller-specific sub-sessions are also included for
students who want to try the same routing shape with F5 NGINX, Traefik,
HAProxy, Contour, Istio, or Cilium.

App images:

```text
prashantdey/appk8stutorial:user-svc-2.0
prashantdey/appk8stutorial:app-svc-2.0
prashantdey/appk8stutorial:frontend-svc-2.0
```

Each microservice has its own folder and Dockerfile under `../../app/`:

- `frontend/frontend.py`: browser UI on port `5000`.
- `user-service/user_service.py`: user API on port `5001`.
- `app-service/app_service.py`: message/application API on port `5002`.

Build the images from the `app` folder:

```bash
docker build -t prashantdey/appk8stutorial:user-svc-2.0 ./user-service
docker build -t prashantdey/appk8stutorial:app-svc-2.0 ./app-service
docker build -t prashantdey/appk8stutorial:frontend-svc-2.0 ./frontend
```

Push those tags before deploying to EKS:

```bash
docker push prashantdey/appk8stutorial:user-svc-2.0
docker push prashantdey/appk8stutorial:app-svc-2.0
docker push prashantdey/appk8stutorial:frontend-svc-2.0
```

The Ingress gives one external address, such as the AWS load balancer DNS name, and routes paths to different internal Services:

```text
http://xyz.com/          -> frontend
http://xyz.com/api/users -> user-service
http://xyz.com/api/apps  -> app-service
```

Here `xyz.com` means the Ingress load balancer address. It can be the AWS ALB DNS name directly, or a custom DNS name that points to it.

## Ingress Controller Selection

For the default EKS path, install the AWS Load Balancer Controller before
applying the ALB Ingress manifest.

Check whether an IngressClass exists:

```bash
kubectl get ingressclass
```

This lesson uses this class by default:

```text
ingressClassName: alb
```

For optional practice, install the controller you want to test and use one of
the optional controller sub-sessions instead of `subsessions/06-ingress`.

| Ingress controller | Good fit | Strong scenarios | Be careful when | Lab class | Practice sub-session |
|---|---|---|---|---|---|
| AWS Load Balancer Controller | Default choice for EKS apps that should use native AWS load balancers. | Public or internal ALB for HTTP/HTTPS, AWS security groups, ACM certificates, WAF integration, ExternalDNS, and NLB for `LoadBalancer` Services. | You need the same manifests to run unchanged outside AWS, or you want an in-cluster proxy layer with advanced gateway features. | `alb` | `subsessions/06-ingress` |
| F5 NGINX Ingress Controller | Teams that want NGINX behavior, NGINX Plus features, or F5 commercial support around Kubernetes ingress. | Standard HTTP routing, TLS termination, NGINX annotations, enterprise support, and environments where NGINX is already the edge standard. | You want cloud-provider-native ALB/NLB provisioning directly from Ingress, or you need service-mesh traffic policy. | `nginx` | `subsessions/07-optional-f5-nginx-ingress` |
| Traefik | Small to medium Kubernetes platforms and developer-heavy teams that want a dynamic edge router with friendly middleware concepts. | Fast lab setup, Let's Encrypt automation, Kubernetes Ingress, Gateway API, CRDs such as `IngressRoute`, dashboards, and API gateway-style middleware. | You need AWS-native ALB features, or the organization standard is NGINX/HAProxy/Envoy. | `traefik` | `subsessions/08-optional-traefik-ingress` |
| HAProxy Ingress | Teams that already trust HAProxy for load balancing and want predictable edge performance and tuning. | HTTP routing, TCP routing, SSL/TLS, header manipulation, rate limiting, and familiar HAProxy operations. | You want Gateway API-first workflows, Envoy-native extension points, or cloud load balancer annotations as the primary interface. | `haproxy` | `subsessions/09-optional-haproxy-ingress` |
| Contour / Envoy | Envoy-based ingress without adopting a full service mesh. | Multi-team clusters, Kubernetes Ingress, Contour `HTTPProxy`, Gateway API, gRPC, Envoy observability, and clean separation between app and platform teams. | You need the broad service-mesh feature set of Istio, or your team is not ready to operate Envoy. | `contour` | `subsessions/10-optional-contour-envoy-ingress` |
| Istio Ingress Gateway | Clusters already using Istio or needing ingress tied to mesh traffic management and security. | mTLS, traffic shifting, retries, timeouts, circuit breaking, authorization policy, telemetry, and Gateway or VirtualService-based routing. | You only need simple north-south HTTP routing; Istio adds control-plane and operating complexity. | `istio` | `subsessions/11-optional-istio-ingress-gateway` |
| Cilium Ingress | Clusters already using Cilium as CNI and wanting ingress integrated with eBPF networking and Cilium policy. | Cilium NetworkPolicy around ingress, Envoy per-node proxying, Gateway API, source IP visibility, and Kubernetes networking/security convergence. | You are not using Cilium, or you want an ingress controller independent of the CNI. | `cilium` | `subsessions/12-optional-cilium-ingress` |

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-shared-config`: create Namespace, ConfigMap, and Secret.
2. `subsessions/02-storageclass`: create the EKS gp3 StorageClass.
3. `subsessions/03-postgres-statefulset`: run PostgreSQL as a StatefulSet.
4. `subsessions/04-api-microservices`: deploy `user-service` and `app-service` as internal Services on different ports.
5. `subsessions/05-frontend`: deploy the frontend as an internal Service.
6. `subsessions/06-ingress`: expose all three Services through one Ingress.
7. Optional: `subsessions/07-optional-f5-nginx-ingress`: expose the same Services through F5 NGINX.
8. Optional: `subsessions/08-optional-traefik-ingress`: expose the same Services through Traefik.
9. Optional: `subsessions/09-optional-haproxy-ingress`: expose the same Services through HAProxy.
10. Optional: `subsessions/10-optional-contour-envoy-ingress`: expose the same Services through Contour and Envoy.
11. Optional: `subsessions/11-optional-istio-ingress-gateway`: expose the same Services through Istio Ingress Gateway.
12. Optional: `subsessions/12-optional-cilium-ingress`: expose the same Services through Cilium Ingress.

## Target Shape By The End

```text
Browser
  -> Ingress /           -> frontend Service    -> frontend Deployment    -> port 5000
  -> Ingress /api/users  -> user-service        -> user-service Deployment -> port 5001
  -> Ingress /api/apps   -> app-service         -> app-service Deployment  -> port 5002

frontend
  -> user-service:5001
  -> app-service:5002

user-service and app-service
  -> PostgreSQL Service
    -> PostgreSQL StatefulSet
      -> PVC from volumeClaimTemplates
```

## Full Apply Order

From `sessions/08-ingress-edge-routing`:

```bash
kubectl apply -f subsessions/01-shared-config/
kubectl apply -f subsessions/02-storageclass/
kubectl apply -f subsessions/03-postgres-statefulset/
kubectl apply -f subsessions/04-api-microservices/
kubectl apply -f subsessions/05-frontend/
kubectl apply -f subsessions/06-ingress/
```

## Optional Ingress Controller Practice

If you want to use another Ingress controller instead of the ALB Ingress,
install that controller first and confirm its `IngressClass`:

```bash
kubectl get ingressclass
```

Then apply one optional manifest instead of the ALB manifest. For example, to
try Traefik:

```bash
kubectl apply -f subsessions/08-optional-traefik-ingress/
```

The optional manifests intentionally omit a host rule, so students can open the
controller load balancer DNS directly in a browser. Each optional sub-session
includes controller installation commands, the `LoadBalancer` Service lookup,
curl tests, and browser-open examples.

## Get The Load Balancer Address

```bash
kubectl get ingress -n app-ingress
```

Wait until the `ADDRESS` column is populated. Then test:

```bash
export APP_DNS=<ingress-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/messages
curl http://$APP_DNS/api/apps/stats
```

Open the frontend:

```text
http://<ingress-address>
```

## Cleanup

From `sessions/08-ingress-edge-routing`:

```bash
kubectl delete -f subsessions/12-optional-cilium-ingress/ --ignore-not-found
kubectl delete -f subsessions/11-optional-istio-ingress-gateway/ --ignore-not-found
kubectl delete -f subsessions/10-optional-contour-envoy-ingress/ --ignore-not-found
kubectl delete -f subsessions/09-optional-haproxy-ingress/ --ignore-not-found
kubectl delete -f subsessions/08-optional-traefik-ingress/ --ignore-not-found
kubectl delete -f subsessions/07-optional-f5-nginx-ingress/ --ignore-not-found
kubectl delete -f subsessions/06-ingress/ --ignore-not-found
kubectl delete -f subsessions/05-frontend/ --ignore-not-found
kubectl delete -f subsessions/04-api-microservices/ --ignore-not-found
kubectl delete -f subsessions/03-postgres-statefulset/ --ignore-not-found
kubectl delete pvc -n app-ingress -l app=postgres,session=ingress --ignore-not-found
kubectl delete -f subsessions/02-storageclass/ --ignore-not-found
kubectl delete -f subsessions/01-shared-config/ --ignore-not-found
```

## Review Questions

1. Why do the frontend and API Services remain `ClusterIP`?
2. What does the Ingress controller create in AWS?
3. Why is `/api/users` routed to a different Service from `/api/apps`?
4. Why does the frontend call APIs by Kubernetes Service DNS inside the cluster?
5. How would a custom domain point to the Ingress load balancer?
6. Which Ingress controller would you choose for an AWS-only production EKS
   app, and why?
7. Which Ingress controller would you choose if the cluster already uses Istio
   or Cilium?
