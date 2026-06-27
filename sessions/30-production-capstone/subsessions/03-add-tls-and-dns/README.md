# Sub-Session 03: Add TLS And DNS

This sub-session exposes the frontend through Gateway API with a TLS listener.

## Goal

Attach a hostname to the frontend Service and terminate HTTPS at the Gateway.

## App-Based Lab

Install a Gateway API controller and cert-manager first. Replace
`message-board.example.com` and the issuer name with values from your cluster.

```bash
kubectl apply -f subsessions/03-add-tls-and-dns/
```

## Check

```bash
kubectl get gateway,httproute,certificate -n message-board-prod
kubectl describe httproute -n message-board-prod message-board
```

## Cleanup

```bash
kubectl delete -f subsessions/03-add-tls-and-dns/ --ignore-not-found
```

## Review Prompts

1. What object owns the listener?
2. What object maps the hostname to the frontend Service?
3. Which controller must create the TLS Secret?
