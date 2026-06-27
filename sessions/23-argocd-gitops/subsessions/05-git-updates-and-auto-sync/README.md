# Sub-Session 05: Git Updates And Auto Sync

This sub-session shows the normal GitOps loop after the first deployment.

Students make a change in GitHub, Argo CD detects that Git and the cluster no
longer match, and then the app is synced again from the UI.

## Start State

Complete sub-sessions 01 through 04 first.

Check the app:

```bash
kubectl get deployment argocd-demo -n argocd-demo
kubectl get pods -n argocd-demo
```

The sample app starts with two replicas.

## Change GitHub

Open this file in the student's GitHub repository:

```text
manifests/app.yml
```

Change the Deployment replica count:

```yaml
replicas: 3
```

Commit the change to `main`.

## Watch Argo CD Detect The Change

Return to the Argo CD UI and open the `argocd-demo` application.

After Argo CD refreshes, the app should show:

```text
OutOfSync
```

If the UI has not refreshed yet, use the refresh button on the application.

## Sync The Git Change

Choose:

```text
SYNC
```

After the sync, check the Deployment:

```bash
kubectl get deployment argocd-demo -n argocd-demo
kubectl get pods -n argocd-demo
```

The Deployment should now have three desired replicas.

## Create Live Drift

Now change the live cluster directly:

```bash
kubectl scale deployment argocd-demo -n argocd-demo --replicas=1
kubectl get deployment argocd-demo -n argocd-demo
```

GitHub still says `replicas: 3`, but the live cluster says one replica. Argo CD
should show the app as `OutOfSync` again.

## Enable Auto Sync And Self-Heal In The UI

Open the app in Argo CD and enable automated sync from the app details or sync
policy settings.

Enable these options:

```text
Auto Sync
Self Heal
Prune Resources
```

After self-heal runs, Argo CD should restore the Deployment to the replica count
from GitHub.

Check again:

```bash
kubectl get deployment argocd-demo -n argocd-demo
```

## Important Detail

Self-heal is powerful because it protects the Git source of truth.

The production habit should be:

```text
Change GitHub -> review -> merge -> Argo CD syncs
```

Avoid:

```text
kubectl edit live objects -> forget to update GitHub
```

## Optional Page Update

Edit the same `manifests/app.yml` file in GitHub and change:

```text
Version: v1
```

to:

```text
Version: v2
```

Commit the change and sync from Argo CD. The page served through the app
port-forward should update after Kubernetes refreshes the ConfigMap volume.

## Review Questions

1. Why did a GitHub commit make the app `OutOfSync`?
2. What happened after syncing the replica change?
3. Why did direct `kubectl scale` create drift?
4. What does self-heal do after live drift?
5. Why should prune be used carefully?
