# Sub-Session 01: Prerequisites And Namespace

This sub-session verifies the autoscaling metrics pipeline and creates the Namespace used by the HPA and VPA labs.

## Why Metrics Server Is Needed

HPA and VPA need recent Pod CPU and memory usage.

Metrics Server collects resource metrics from kubelets and exposes them through the Kubernetes Metrics API:

```text
metrics.k8s.io
```

HPA reads this API to decide replica count. VPA reads this API to generate resource recommendations.

## Check Metrics Server

Run:

```bash
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl top nodes
kubectl top pods --all-namespaces
```

Expected result:

- The APIService should be available.
- `kubectl top nodes` should show CPU and memory usage.
- `kubectl top pods` should show Pod usage.

If these commands work, continue to the Namespace step.

## Install Metrics Server If Missing

For EKS, you can install the community Metrics Server add-on:

```bash
export CLUSTER_NAME=demo-batch16a
export AWS_REGION=us-east-2

aws eks describe-addon-versions \
  --addon-name metrics-server \
  --region "$AWS_REGION"

eksctl create addon \
  --cluster "$CLUSTER_NAME" \
  --name metrics-server \
  --region "$AWS_REGION"
```

If you are not using EKS add-ons, install the upstream manifest:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Verify:

```bash
kubectl get deployment metrics-server -n kube-system
kubectl rollout status deployment/metrics-server -n kube-system
kubectl top nodes
```

## Create Namespace

From `sessions/12-pod-autoscaling`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
```

Check:

```bash
kubectl get namespace app-autoscaling
```

## Cleanup

Only delete this Namespace after the HPA and VPA labs are finished:

```bash
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
```

Do not delete Metrics Server unless you are sure no other HPA, VPA, dashboard, or metrics lab needs it.
