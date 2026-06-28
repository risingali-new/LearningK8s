# Sub-Session 03: VPA Installation

This sub-session installs or verifies Vertical Pod Autoscaler.

VPA is different from HPA:

- HPA is part of the Kubernetes autoscaling API.
- VPA is installed separately as CRDs, RBAC, Deployments, and a mutating admission webhook.

## Check Whether VPA Is Already Installed

```bash
kubectl api-resources | grep -i vertical
kubectl get crd | grep verticalpodautoscalers
kubectl get pods -n kube-system | grep vpa
```

Expected resources include:

```text
verticalpodautoscalers.autoscaling.k8s.io
vpa-recommender
vpa-updater
vpa-admission-controller
```

If they exist and are healthy, continue to `subsessions/04-vpa-recommendations`.

## Install VPA

The official VPA repository installs VPA by running helper scripts from the source tree.

On Linux, macOS, WSL, Git Bash, or AWS CloudShell:

```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

The script creates:

- VPA CRDs.
- RBAC permissions.
- VPA recommender.
- VPA updater.
- VPA admission controller.
- Admission webhook certificates.

Verify:

```bash
kubectl get crd | grep verticalpodautoscalers
kubectl get pods -n kube-system | grep vpa
kubectl api-resources | grep -i vertical
```

## Metrics Server Requirement

VPA also needs Metrics Server.

Check:

```bash
kubectl top pods --all-namespaces
kubectl get apiservice v1beta1.metrics.k8s.io
```

If metrics are missing, go back to:

```text
subsessions/01-prerequisites-and-namespace/README.md
```

## VPA Version Compatibility

Before installing VPA for a real cluster, check the compatibility table in the official VPA installation documentation.

The lab cluster in this repository is designed around modern EKS/Kubernetes versions, and the current VPA API used here is:

```text
autoscaling.k8s.io/v1
```

## Tear Down VPA

Only remove VPA if you installed it just for this lab and no other workload needs it.

From the cloned VPA source directory:

```bash
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-down.sh
```

Then verify:

```bash
kubectl get pods -n kube-system | grep vpa
kubectl get crd | grep verticalpodautoscalers
```

If the commands return nothing, VPA has been removed.

## Teaching Notes

Start VPA in recommendation mode first.

This keeps the lesson safe because students can inspect what VPA would do before allowing it to evict or mutate Pods.
