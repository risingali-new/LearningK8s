#!/bin/bash

set -e

echo "====================================="
echo "Deploying Core Kubernetes Resources"
echo "====================================="

kubectl apply -f sessions/01-core-k8s/subsessions/01-namespace/01-namespace.yml

kubectl apply -f sessions/01-core-k8s/subsessions/02-configmap-secret/01-app-configmap.yml
kubectl apply -f sessions/01-core-k8s/subsessions/02-configmap-secret/02-app-secret.yml

kubectl apply -f sessions/01-core-k8s/subsessions/03-postgres-deployment-service/01-postgres-deployment.yml
kubectl apply -f sessions/01-core-k8s/subsessions/03-postgres-deployment-service/02-postgres-service.yml

kubectl apply -f sessions/01-core-k8s/subsessions/04-flask-pod/01-flask-pod.yml

kubectl apply -f sessions/01-core-k8s/subsessions/05-flask-deployment/01-flask-deployment.yml

kubectl apply -f sessions/01-core-k8s/subsessions/06-flask-services/01-flask-service-clusterip.yml
kubectl apply -f sessions/01-core-k8s/subsessions/06-flask-services/02-flask-service-nodeport.yml
kubectl apply -f sessions/01-core-k8s/subsessions/06-flask-services/03-flask-service-loadbalancer.yml


echo "====================================="
echo "Deploying Storage Resources"
echo "====================================="

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/01-storage-problem-and-shared-config/01-namespace.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/01-storage-problem-and-shared-config/02-app-configmap.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/01-storage-problem-and-shared-config/03-app-secret.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/02-static-pv-pvc/01-static-pv-hostpath.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/02-static-pv-pvc/02-postgres-pvc-static.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/03-postgres-with-static-pvc/01-postgres-deployment-static-pvc.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/03-postgres-with-static-pvc/02-postgres-service-static.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/04-flask-with-persistent-db/01-flask-deployment.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/04-flask-with-persistent-db/02-flask-service.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/05-storageclass/01-storageclass-aws-ebs-gp3.yml

kubectl apply -f sessions/02-storage-pv-pvc-statefulset/subsessions/06-postgres-statefulset/01-postgres-statefulset-dynamic.yml


echo "====================================="
echo "Deployment Completed"
echo "====================================="

echo ""
echo "Verifying Resources..."
echo ""

kubectl get ns

echo ""
kubectl get pods -A

echo ""
kubectl get svc -A

echo ""
kubectl get pvc -A

echo ""
kubectl get pv