# Sub-Session 06: NetworkPolicy Lab

This sub-session creates a small frontend and backend, tests connectivity, then
uses NetworkPolicy to restrict ingress to the backend.

## Important Requirement

NetworkPolicy enforcement requires a policy-capable CNI.

Examples that can enforce policy:

- Calico.
- Cilium.
- Antrea.
- Weave Net.
- EKS with policy support configured.

Plain Flannel by itself does not enforce Kubernetes NetworkPolicy.

If the cluster accepts the YAML but traffic behavior does not change, the CNI is
probably not enforcing NetworkPolicy.

## What This Lab Creates

```text
cni-lab Namespace

frontend Deployment
  -> BusyBox container used as a curl/wget client

backend Deployment
  -> BusyBox httpd server on port 8080

backend Service
  -> ClusterIP in front of backend Pods

NetworkPolicies
  -> default deny ingress for all Pods
  -> allow frontend Pods to call backend Pods on TCP 8080
```

## Apply Baseline Workloads

From `sessions/18-cni-networking`:

```bash
kubectl apply -f subsessions/06-network-policy/01-namespace.yml
kubectl apply -f subsessions/06-network-policy/02-connectivity-demo.yml
```

Wait for Pods:

```bash
kubectl wait --for=condition=Available deployment/frontend -n cni-lab --timeout=120s
kubectl wait --for=condition=Available deployment/backend -n cni-lab --timeout=120s
kubectl get pods -n cni-lab -o wide
```

## Test Baseline Connectivity

From frontend to backend Service:

```bash
kubectl exec -n cni-lab deploy/frontend -- wget -qO- http://backend.cni-lab.svc.cluster.local:8080
```

Expected output:

```text
backend-ok
```

Also inspect the Service and EndpointSlice:

```bash
kubectl get service backend -n cni-lab
kubectl get endpointslice -n cni-lab -l kubernetes.io/service-name=backend
```

## Apply Default Deny Ingress

```bash
kubectl apply -f subsessions/06-network-policy/03-default-deny-ingress.yml
```

Test again:

```bash
kubectl exec -n cni-lab deploy/frontend -- wget -T 3 -qO- http://backend.cni-lab.svc.cluster.local:8080
```

Expected behavior with a policy-capable CNI:

```text
The request should time out or fail.
```

If it still succeeds, pause and discuss CNI policy support.

## Allow Frontend To Backend

```bash
kubectl apply -f subsessions/06-network-policy/04-allow-frontend-to-backend.yml
```

Test again:

```bash
kubectl exec -n cni-lab deploy/frontend -- wget -qO- http://backend.cni-lab.svc.cluster.local:8080
```

Expected output:

```text
backend-ok
```

## Read The Policy

The allow policy selects destination Pods:

```text
role=backend
```

It allows ingress from source Pods:

```text
role=frontend
```

Only on:

```text
TCP 8080
```

The policy is about traffic into the selected backend Pods. It does not give
the frontend a general permission to reach everything.

## Important Policy Rules

NetworkPolicy is additive.

If a Pod is selected by at least one ingress policy, ingress traffic is denied
unless some policy allows it.

If a Pod is not selected by any ingress policy, ingress traffic is allowed by
default.

The same pattern applies separately to egress policies.

## Cleanup

From `sessions/18-cni-networking`:

```bash
kubectl delete -f subsessions/06-network-policy/04-allow-frontend-to-backend.yml --ignore-not-found
kubectl delete -f subsessions/06-network-policy/03-default-deny-ingress.yml --ignore-not-found
kubectl delete -f subsessions/06-network-policy/02-connectivity-demo.yml --ignore-not-found
kubectl delete -f subsessions/06-network-policy/01-namespace.yml --ignore-not-found
```

## Review Questions

1. Why does Kubernetes accept NetworkPolicy objects even when a CNI does not enforce them?
2. What changed after the default deny ingress policy?
3. Why does the allow policy select backend Pods instead of frontend Pods?
4. What does "NetworkPolicy is additive" mean?
5. How would you allow only DNS egress from a namespace?
