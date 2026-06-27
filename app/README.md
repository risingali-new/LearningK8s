# Kubernetes Message Board App

This is the sample application used throughout the Kubernetes learning sessions.

The application folder owns only the app source code and Docker assets. Kubernetes manifests are intentionally kept outside this folder under `../sessions/` so each Kubernetes topic can introduce its own YAML step by step.

## Architecture

The app can run in two shapes.

Earlier sessions use the monolith entrypoint:

```text
Browser UI -> app.py on port 5000 -> PostgreSQL database
```

The ingress session uses separate microservice folders and separate images:

```text
Browser UI -> frontend/frontend.py on port 5000
frontend -> user-service/user_service.py on port 5001 -> PostgreSQL
frontend -> app-service/app_service.py on port 5002 -> PostgreSQL

Ingress /          -> frontend
Ingress /api/users -> user-service
Ingress /api/apps  -> app-service
```

## Entrypoints

| File | Purpose | Port |
| --- | --- | --- |
| `app/app.py` | Original monolith used by Sessions 02 and 07. | `5000` |
| `frontend/frontend.py` | Browser UI used by Session 08. | `5000` |
| `user-service/user_service.py` | User API used by Session 08. | `5001` |
| `app-service/app_service.py` | Message/application API used by Session 08. | `5002` |

## Folder Structure

```text
app/
  app-service/
    app_service.py
    database.py
    Dockerfile
    requirements.txt
  frontend/
    frontend.py
    Dockerfile
    requirements.txt
    static/
    templates/
  user-service/
    user_service.py
    database.py
    Dockerfile
    requirements.txt
  app/
    app.py
    database.py
    requirements.txt
    static/
    templates/
  Dockerfile              # legacy monolith image for Sessions 02 and 07
  docker-compose.yml
```

## Local Development With Docker Compose

From this folder:

```bash
docker compose up --build
```

Open the frontend:

```text
http://localhost:5000
```

API endpoints:

```text
http://localhost:5001/api/users
http://localhost:5001/api/users/stats
http://localhost:5002/api/apps
http://localhost:5002/api/apps/messages
http://localhost:5002/api/apps/stats
```

Stop the local environment:

```bash
docker compose down
```

Remove the local PostgreSQL volume too:

```bash
docker compose down -v
```

## Build The Service Images

```bash
docker build -t prashantdey/appk8stutorial:1.0 .
docker build -t prashantdey/appk8stutorial:user-svc-2.0 ./user-service
docker build -t prashantdey/appk8stutorial:app-svc-2.0 ./app-service
docker build -t prashantdey/appk8stutorial:frontend-svc-2.0 ./frontend
```

## Push To Docker Hub For EKS

Login:

```bash
docker login
```

Push the service image tags:

```bash
docker push prashantdey/appk8stutorial:1.0
docker push prashantdey/appk8stutorial:user-svc-2.0
docker push prashantdey/appk8stutorial:app-svc-2.0
docker push prashantdey/appk8stutorial:frontend-svc-2.0
```

The Kubernetes Session 08 ingress manifests use these image names:

```text
prashantdey/appk8stutorial:user-svc-2.0
prashantdey/appk8stutorial:app-svc-2.0
prashantdey/appk8stutorial:frontend-svc-2.0
```

## App Configuration

Database-backed entrypoints read these environment variables:

| Variable | Purpose | Example |
| --- | --- | --- |
| `DB_HOST` | PostgreSQL hostname | `postgres` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `appdb` |
| `DB_USER` | Database username | `appuser` |
| `DB_PASSWORD` | Database password | `apppassword` |
| `FLASK_SECRET_KEY` | Flask session secret for UI entrypoints | `change-this` |

Frontend reads these service URLs:

| Variable | Purpose | Example |
| --- | --- | --- |
| `USER_SERVICE_URL` | Internal URL for the user API | `http://user-service:5001/api/users` |
| `APP_SERVICE_URL` | Internal URL for the app API | `http://app-service:5002/api/apps` |
| `USER_SERVICE_HEALTH_URL` | Readiness URL for user-service | `http://user-service:5001/readyz` |
| `APP_SERVICE_HEALTH_URL` | Readiness URL for app-service | `http://app-service:5002/readyz` |

Health endpoints:

- `/healthz`: process health check.
- `/readyz`: database or downstream service readiness check.
- `/metrics`: Prometheus text metrics used by the observability sessions.

API endpoints:

- `/api/users`: list or create users.
- `/api/users/stats`: user count.
- `/api/apps`: app-service info.
- `/api/apps/messages`: list or create messages.
- `/api/apps/stats`: message count.

## Kubernetes Sessions

Kubernetes examples for this app are kept in:

```text
../sessions/
```

Current sessions that introduce the app most directly:

- `sessions/02-core-k8s`: Namespace, Pod, Deployment, Service, labels, selectors, and basic troubleshooting.
- `sessions/07-storage-pv-pvc-statefulset`: PV, PVC, StorageClass, StatefulSet, and database persistence.
- `sessions/08-ingress-edge-routing`: frontend, user-service, app-service, and Ingress path routing.
- `sessions/30-production-capstone`: production-style delivery of the complete app.
