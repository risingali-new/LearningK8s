# Sub-Session 06: Cleanup

This sub-session removes the UI-created Argo CD app and, if the lab is finished,
Argo CD itself.

## Delete The Argo CD Application From The UI

Open the Argo CD UI:

```text
https://localhost:8080
```

Open the `argocd-demo` application and choose:

```text
DELETE
```

If Argo CD asks whether to delete child resources, choose cascading deletion.
That lets Argo CD remove the Deployment, Service, and ConfigMap it created from
GitHub.

## Check For Remaining Demo Resources

```bash
kubectl get all -n argocd-demo
```

If the Namespace still exists, delete it:

```bash
kubectl delete namespace argocd-demo --ignore-not-found
```

## Remove Argo CD

Only do this if no other lessons or apps are using Argo CD:

```bash
kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --ignore-not-found
kubectl delete -f subsessions/01-prerequisites-and-install/01-argocd-namespace.yml --ignore-not-found
```

## GitHub Repository Cleanup

The student's GitHub repository can be kept for review or deleted from GitHub:

```text
argocd-demo-app
```

Keeping it is useful because it shows the Git history behind the Argo CD lab.

## Final Check

```bash
kubectl get namespace argocd argocd-demo
kubectl get crd | grep argoproj.io
```

The namespace and CRD commands may show `NotFound` or no `argoproj.io` output
after cleanup. That is expected if Argo CD was removed.

## Review Questions

1. Why should the UI-created application be deleted before removing Argo CD?
2. What does cascading deletion remove?
3. Why should shared Argo CD installations not be deleted casually?
