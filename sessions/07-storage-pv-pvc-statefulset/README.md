# Session 07: Persistent Storage, PV/PVC, StorageClass, And StatefulSet

This session continues the same Flask/PostgreSQL sample app from Session 02, but focuses on persistent storage and the Kubernetes controller that fits stateful workloads.

App image:

```text
prashantdey/appk8stutorial:1.0
```

The key teaching idea is:

```text
Flask is stateless -> Deployment
PostgreSQL is stateful -> persistent storage and StatefulSet
```

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-storage-problem-and-shared-config`: explain the storage problem and create Namespace, ConfigMap, and Secret.
2. `subsessions/02-static-pv-pvc`: create a static `hostPath` PV and a PostgreSQL PVC.
3. `subsessions/03-postgres-with-static-pvc`: run PostgreSQL with the PVC and prove storage survives Pod replacement.
4. `subsessions/04-flask-with-persistent-db`: connect the Flask app to the persistent PostgreSQL database.
5. `subsessions/05-storageclass`: introduce dynamic provisioning with an EKS gp3 StorageClass.
6. `subsessions/06-postgres-statefulset`: replace the database Deployment with a StatefulSet and `volumeClaimTemplates`.

## Target Shape By The End

```text
Browser
  -> Flask Service
    -> Flask Deployment
      -> PostgreSQL Service
        -> PostgreSQL StatefulSet
          -> PVC from volumeClaimTemplates
            -> PV created by StorageClass
```

## Part 1: Static PV/PVC Apply Order

From `sessions/07-storage-pv-pvc-statefulset`:

```bash
kubectl apply -f subsessions/01-storage-problem-and-shared-config/
kubectl apply -f subsessions/02-static-pv-pvc/
kubectl apply -f subsessions/03-postgres-with-static-pvc/
kubectl apply -f subsessions/04-flask-with-persistent-db/
```

Use this part to show the mechanics:

- PV is the storage resource.
- PVC is the request for storage.
- PostgreSQL mounts the PVC.
- Data survives a Pod replacement because the data is outside the container filesystem.

## Part 2: StatefulSet Apply Order

For EKS dynamic storage:

```bash
kubectl apply -f subsessions/01-storage-problem-and-shared-config/
kubectl apply -f subsessions/05-storageclass/
kubectl apply -f subsessions/06-postgres-statefulset/
kubectl apply -f subsessions/04-flask-with-persistent-db/
```

If the static PostgreSQL Deployment is still running, remove it before applying the StatefulSet:

```bash
kubectl delete -f subsessions/03-postgres-with-static-pvc/ --ignore-not-found
```

If the cluster already has a suitable default StorageClass, you can still use the provided gp3 StorageClass for explicit teaching.

## Cleanup

From `sessions/07-storage-pv-pvc-statefulset`:

```bash
kubectl delete -f subsessions/04-flask-with-persistent-db/ --ignore-not-found
kubectl delete -f subsessions/06-postgres-statefulset/ --ignore-not-found
kubectl delete pvc -n app-storage -l app=postgres,storage-demo=stateful --ignore-not-found
kubectl delete -f subsessions/05-storageclass/ --ignore-not-found
kubectl delete -f subsessions/03-postgres-with-static-pvc/ --ignore-not-found
kubectl delete -f subsessions/02-static-pv-pvc/ --ignore-not-found
kubectl delete -f subsessions/01-storage-problem-and-shared-config/ --ignore-not-found
```

## Review Questions

1. Why does PostgreSQL need persistent storage?
2. What is the difference between a PV and a PVC?
3. Why is `hostPath` useful for learning but risky for production?
4. What does a StorageClass add?
5. Why does a StatefulSet fit PostgreSQL better than a normal Deployment?
6. Why does a StatefulSet need a headless Service?
7. Why are StatefulSet PVCs retained after the StatefulSet is deleted?
