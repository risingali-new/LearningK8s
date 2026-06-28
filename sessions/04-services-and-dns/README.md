# Session 04: Services And DNS

This session separates Service and DNS behavior from the basic app deployment.

## Sub-Session Order

1. `01-service-selectors`: labels, selectors, and Endpoints.
2. `02-clusterip`: stable internal virtual IP and DNS.
3. `03-nodeport`: exposing a Service on every node.
4. `04-loadbalancer`: cloud load balancer provisioning.
5. `05-coredns`: Kubernetes DNS names and lookup flow.
6. `06-endpoints-and-endpointslices`: how Services find backing Pods.
7. `07-service-troubleshooting`: selector mismatch, no endpoints, DNS failures.

## Existing Material To Reuse

- Service manifests: `sessions/02-core-k8s/subsessions/06-flask-services`
- Service traffic internals: `sessions/18-cni-networking/subsessions/03-pod-traffic-and-services`

## Useful Commands

```bash
kubectl get svc -A
kubectl get endpoints -A
kubectl get endpointslice -A
kubectl describe svc <service-name> -n <namespace>
kubectl exec -n <namespace> <pod-name> -- nslookup <service-name>
```

## Review Questions

1. How does a Service choose Pods?
2. What is the difference between ClusterIP, NodePort, and LoadBalancer?
3. Why can a Service exist with no endpoints?
4. What DNS name does Kubernetes create for a Service?
