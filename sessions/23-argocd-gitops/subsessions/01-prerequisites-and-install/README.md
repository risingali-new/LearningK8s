# Sub-Session 01: Argo CD Prerequisites And Install

This sub-session installs Argo CD into the `argocd` Namespace and opens the UI.

Argo CD is usually installed as a set of Kubernetes controllers, API services,
CRDs, and RBAC objects. For this lab, use the official upstream install
manifests so students can focus on the GitOps workflow.

The Argo CD install includes its own CRDs, but this session does not ask
students to create Argo CD `Application` YAML by hand. The application is created
from the UI in a later sub-session.

## Create The Namespace

From `sessions/23-argocd-gitops`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-install/01-argocd-namespace.yml
```

## Install Argo CD

```bash
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

The lab uses `stable` to keep the classroom setup simple. For production, pin a
specific Argo CD release tag and upgrade intentionally.

Server-side apply is used because some Argo CD CRDs are large enough to be
awkward for client-side apply.

## Check The Install

```bash
kubectl get pods -n argocd
kubectl get services -n argocd
kubectl get crd | grep argoproj.io
```

Wait for the main API server deployment:

```bash
kubectl wait --for=condition=Available deployment/argocd-server -n argocd --timeout=180s
```

## Access The UI

For a classroom lab, port-forwarding avoids creating a public load balancer:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open:

```text
https://localhost:8080
```

The certificate is self-signed, so the browser will show a warning.

## Initial Admin Password

If the Argo CD CLI is installed:

```bash
argocd admin initial-password -n argocd
```

Without the CLI:

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

Login user:

```text
admin
```

With the port-forward running, login from another terminal:

```bash
argocd login localhost:8080 --username admin --password <PASSWORD> --insecure
```

After changing the admin password, delete the initial password Secret:

```bash
kubectl delete secret argocd-initial-admin-secret -n argocd --ignore-not-found
```

## Important Detail

Argo CD is not only a UI. The useful part is the control loop:

```text
Git desired state != live Kubernetes state
  -> Argo CD marks the app OutOfSync
  -> user or automation syncs the app
  -> live state matches Git again
```

## Cleanup

Do not clean up yet if continuing to the next sub-session.

To remove only this install:

```bash
kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --ignore-not-found
kubectl delete -f subsessions/01-prerequisites-and-install/01-argocd-namespace.yml --ignore-not-found
```

## Review Questions

1. Why is Argo CD installed into its own Namespace?
2. Why is port-forwarding useful for a lab?
3. What does the `argocd-server` service provide?
4. Why should production use a pinned Argo CD release?
