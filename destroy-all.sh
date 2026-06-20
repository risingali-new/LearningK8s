#!/bin/bash

kubectl delete -f sessions/02-storage-pv-pvc-statefulset/subsessions/06-postgres-statefulset/ --ignore-not-found=true

kubectl delete -f sessions/02-storage-pv-pvc-statefulset/subsessions/05-storageclass/ --ignore-not-found=true

kubectl delete -f sessions/02-storage-pv-pvc-statefulset/subsessions/04-flask-with-persistent-db/ --ignore-not-found=true

kubectl delete -f sessions/02-storage-pv-pvc-statefulset/subsessions/03-postgres-with-static-pvc/ --ignore-not-found=true

kubectl delete -f sessions/02-storage-pv-pvc-statefulset/subsessions/02-static-pv-pvc/ --ignore-not-found=true

kubectl delete -f sessions/01-core-k8s/subsessions/06-flask-services/ --ignore-not-found=true

kubectl delete -f sessions/01-core-k8s/subsessions/05-flask-deployment/ --ignore-not-found=true

kubectl delete -f sessions/01-core-k8s/subsessions/04-flask-pod/ --ignore-not-found=true

kubectl delete -f sessions/01-core-k8s/subsessions/03-postgres-deployment-service/ --ignore-not-found=true

echo "Cleanup completed"