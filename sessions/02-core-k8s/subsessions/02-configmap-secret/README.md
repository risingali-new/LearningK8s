# Sub-Session 02: ConfigMap And Secret

This sub-session adds configuration and credentials for the Flask/PostgreSQL app.

## Why ConfigMap Is Used

A ConfigMap stores non-secret configuration outside the container image.

For this app, Flask needs to know:

- PostgreSQL service name.
- PostgreSQL port.

Those values can change between environments, so they should not be hardcoded into the image.

## Why Secret Is Used

A Secret stores sensitive values such as passwords and application keys.

For this app, the Secret stores:

- Database name.
- Database user.
- Database password.
- Flask secret key.

This keeps credentials out of the Docker image and out of plain application code.

## How Kubernetes Uses Them

Pods read ConfigMaps and Secrets as environment variables.

PostgreSQL reads:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

Flask reads:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `FLASK_SECRET_KEY`

## Manifests

```text
01-app-configmap.yml
02-app-secret.yml
```

## Apply

Run the namespace sub-session first.

From `sessions/02-core-k8s`:

```bash
kubectl apply -f subsessions/02-configmap-secret/
```

## Check

```bash
kubectl get configmap -n app-core
kubectl describe configmap app-config -n app-core
kubectl get secret -n app-core
kubectl describe secret app-secrets -n app-core
```

Do not expect application Pods yet. This step only prepares configuration for later workloads.

