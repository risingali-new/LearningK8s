# Session 09: Gateway API And TLS

This session introduces the modern Kubernetes Gateway API and HTTPS automation.

## Sub-Session Order

1. `01-gateway-api-concepts`: GatewayClass, Gateway, HTTPRoute.
2. `02-install-gateway-controller`: choose ALB, Envoy Gateway, Traefik, Istio, or Cilium.
3. `03-http-route`: route traffic to frontend and APIs.
4. `04-tls-termination`: attach certificates to Gateway listeners.
5. `05-cert-manager`: automate certificate requests.
6. `06-externaldns`: automate public DNS records.
7. `07-migration-from-ingress`: when to keep Ingress and when to use Gateway API.

## Existing Material To Reuse

- Ingress controller comparison: `sessions/08-ingress-edge-routing`

## Review Questions

1. What problem does Gateway API solve beyond Ingress?
2. What is the difference between GatewayClass and Gateway?
3. What does HTTPRoute own?
4. Why are cert-manager and ExternalDNS usually platform-level components?
