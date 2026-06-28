# Sub-Session 02: Create A GitHub Repository

This sub-session creates the Git repository that Argo CD will watch.

The important teaching point is:

```text
Do not apply this app YAML with kubectl.
Commit it to GitHub and let Argo CD apply it.
```

## Create The Repository

In GitHub, create a new repository:

```text
argocd-demo-app
```

For the classroom lab, make it public so Argo CD can read it without repository
credentials. Private repositories also work, but require adding credentials in
Argo CD.

## Add The Manifest File

Create this path in the GitHub repository:

```text
manifests/app.yml
```

Copy the sample file from this training repo:

```text
sessions/23-argocd-gitops/subsessions/02-create-github-repository/sample-repo/manifests/app.yml
```

Commit the file to the repository's `main` branch.

The final GitHub repository should look like this:

```text
argocd-demo-app
`-- manifests
    `-- app.yml
```

## Optional Local Git Flow

If students prefer using Git locally:

```bash
mkdir argocd-demo-app
cd argocd-demo-app
mkdir manifests
copy D:\teaching\batch16A\k8s\sessions\23-argocd-gitops\subsessions\02-create-github-repository\sample-repo\manifests\app.yml manifests\app.yml
git init
git add manifests/app.yml
git commit -m "Add Argo CD demo app"
git branch -M main
git remote add origin https://github.com/<GITHUB_USERNAME>/argocd-demo-app.git
git push -u origin main
```

Replace `<GITHUB_USERNAME>` with the student's GitHub username.

## What The YAML Creates

The sample `app.yml` file contains three Kubernetes objects:

| Object | Purpose |
| --- | --- |
| ConfigMap | Stores a simple `index.html` page |
| Deployment | Runs two nginx Pods |
| Service | Exposes the Pods inside the cluster |

## Important Detail

Argo CD needs a repository URL and a path.

For this lab:

```text
Repository URL:
  https://github.com/<GITHUB_USERNAME>/argocd-demo-app.git

Path:
  manifests
```

The next sub-session uses these values in the Argo CD UI.

## Review Questions

1. Why are we committing YAML to GitHub instead of applying it with `kubectl`?
2. Why should the lab repository be public unless credentials are configured?
3. What path should Argo CD read from the repository?
4. Which Kubernetes objects are defined in the sample file?
