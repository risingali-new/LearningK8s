# Session 27: Service Mesh

This session covers service-to-service traffic management and security.

## Sub-Session Order

1. `01-service-mesh-concepts`: data plane, control plane, sidecars, ambient modes.
2. `02-install-istio-or-linkerd`: choose one mesh for the lab.
3. `03-mtls`: service identity and encryption.
4. `04-traffic-management`: retries, timeouts, traffic splitting.
5. `05-circuit-breaking`: protect dependencies.
6. `06-mesh-observability`: telemetry, traces, service graph.
7. `07-mesh-tradeoffs`: when not to use a mesh.

## Existing Material To Reuse

- Istio ingress gateway intro: `sessions/08-ingress-edge-routing/subsessions/11-optional-istio-ingress-gateway`

## Review Questions

1. What does a service mesh add beyond Services and Ingress?
2. What is mTLS?
3. Why can retries be dangerous without limits?
4. What is the operational cost of a mesh?
