# Session 12: Pod Autoscaling With HPA And VPA

This session explains Kubernetes application autoscaling with Horizontal Pod Autoscaler and Vertical Pod Autoscaler.

The main teaching idea is:

```text
HPA changes how many Pods run.
VPA changes, or recommends, how much CPU and memory each Pod requests.
Cluster autoscaling changes how many Nodes exist.
```

This session focuses on HPA and VPA. Cluster Autoscaler, Karpenter, and EKS Auto Mode node scaling are related topics, but they are not the main lab here.

## Autoscaling Layers

```text
Incoming traffic or workload
  -> HPA decides replica count
    -> Deployment creates or removes Pods
      -> Scheduler places Pods on Nodes
        -> If there is not enough Node capacity, node autoscaling may add Nodes

Observed CPU and memory usage
  -> VPA calculates resource recommendations
    -> VPA may only report recommendations
    -> or VPA may apply requests when Pods are created or recreated
```

## HPA In One Line

Horizontal Pod Autoscaler watches metrics and updates the `replicas` value of a scalable resource such as a Deployment, ReplicaSet, or StatefulSet.

Example:

```text
If one Pod is too busy, run more Pods.
```

HPA is best for stateless workloads where more replicas can share traffic.

## VPA In One Line

Vertical Pod Autoscaler watches CPU and memory usage and recommends, or applies, better container resource requests.

Example:

```text
If one Pod was given too little CPU or memory, give each Pod a bigger request.
```

VPA is useful for right-sizing workloads and preventing under-requested or over-requested Pods.

## Why Resource Requests Matter

Autoscaling decisions depend heavily on `resources.requests`.

For CPU-based HPA, utilization is calculated against the requested CPU:

```text
CPU utilization percentage = current CPU usage / requested CPU
```

If a container requests `100m` CPU and currently uses `80m`, Kubernetes treats that as:

```text
80m / 100m = 80% CPU utilization
```

If the HPA target is `50%`, this Pod is above target, so HPA may add replicas.

Without CPU requests, CPU utilization based HPA cannot calculate the percentage correctly.

## HPA Formula

Kubernetes uses this basic ratio:

```text
desiredReplicas = ceil(currentReplicas * currentMetricValue / desiredMetricValue)
```

Example:

```text
currentReplicas = 2
current average CPU utilization = 90%
target average CPU utilization = 50%

desiredReplicas = ceil(2 * 90 / 50)
desiredReplicas = ceil(3.6)
desiredReplicas = 4
```

The HPA controller then updates the Deployment replica count, and the Deployment creates the extra Pods.

## VPA Components

VPA is not installed by default in Kubernetes. It is installed as extra cluster components and a CRD.

The VPA system has three major parts:

- Recommender: reads historical and current usage, then writes recommendations into the VPA object status.
- Updater: decides whether existing Pods should be evicted so new Pods can get updated requests.
- Admission controller: mutates new Pods at creation time so they start with VPA-recommended requests.

## VPA Update Modes

VPA supports several update modes:

- `Off`: only generate recommendations. This is the safest mode for learning and production analysis.
- `Initial`: apply recommendations only when Pods are first created.
- `Recreate`: evict Pods when the recommendations need to be applied.
- `InPlace` and `InPlaceOrRecreate`: apply changes without eviction when supported by the cluster and VPA feature gates.

In this session, use `Off` first. Use `Recreate` only after students understand that VPA can restart Pods.

## HPA And VPA Together

Do not blindly run CPU-based HPA and CPU-managing VPA on the same Deployment.

Reason:

```text
HPA reads CPU utilization as usage divided by request.
VPA changes the CPU request.
Changing the request changes the percentage HPA sees.
```

This can create confusing scaling behavior.

Common production patterns:

- Use HPA for replica scaling and VPA in `Off` mode for recommendations.
- Use HPA on external or custom business metrics, and VPA for CPU/memory request sizing.
- Use VPA for workloads that should not scale horizontally.
- Use node autoscaling separately so the cluster can add capacity when HPA creates more Pods.

## Prerequisites

You need:

- A working Kubernetes cluster.
- `kubectl` configured for the cluster.
- Metrics Server installed and working.
- Enough node capacity for extra Pods.
- VPA installed before the VPA sub-session.

Check metrics:

```bash
kubectl top nodes
kubectl top pods --all-namespaces
kubectl get apiservice v1beta1.metrics.k8s.io
```

If those commands do not work, finish `subsessions/01-prerequisites-and-namespace` before starting HPA.

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-prerequisites-and-namespace`: verify Metrics Server and create the lab Namespace.
2. `subsessions/02-hpa-cpu-autoscaling`: scale a Deployment horizontally from CPU load.
3. `subsessions/03-vpa-installation`: install or verify the VPA system components.
4. `subsessions/04-vpa-recommendations`: generate VPA recommendations and optionally apply them with `Recreate`.
5. `subsessions/05-hpa-vpa-production-patterns`: discuss when to use HPA, VPA, or both.
6. `subsessions/06-memory-hpa`: scale a Deployment from memory utilization.
7. `subsessions/07-custom-external-metrics-hpa`: study custom and external metric HPA patterns.
8. KEDA follow-up: add event-driven scaling later.

## Target Shape By The End

```text
HPA lab:

load-generator Deployment
  -> cpu-demo Service
    -> cpu-demo Deployment
      -> HPA watches CPU metrics
        -> HPA updates Deployment replicas

VPA lab:

vpa-load-generator Deployment
  -> vpa-demo Service
    -> vpa-demo Deployment
      -> VPA watches CPU and memory metrics
        -> VPA writes recommendations
        -> optional Recreate mode updates future Pods

Advanced HPA labs:

memory-load-generator Deployment
  -> memory-demo Deployment
    -> HPA watches memory utilization

custom-metric demo
  -> app exposes /metrics
    -> Prometheus adapter exposes custom metrics API
      -> HPA reads custom or external metrics
```

## Full Apply Order

From `sessions/12-pod-autoscaling`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
kubectl apply -f subsessions/02-hpa-cpu-autoscaling/01-cpu-demo-deployment.yml
kubectl apply -f subsessions/02-hpa-cpu-autoscaling/02-cpu-demo-hpa.yml
kubectl apply -f subsessions/02-hpa-cpu-autoscaling/03-load-generator.yml
```

Watch HPA:

```bash
kubectl get hpa -n app-autoscaling -w
```

After the HPA lab, stop its load generator before moving to the VPA lab:

```bash
kubectl delete -f subsessions/02-hpa-cpu-autoscaling/03-load-generator.yml --ignore-not-found
```

Install VPA by following:

```text
subsessions/03-vpa-installation/README.md
```

Then run the VPA lab:

```bash
kubectl apply -f subsessions/04-vpa-recommendations/01-vpa-demo-deployment.yml
kubectl apply -f subsessions/04-vpa-recommendations/02-vpa-recommendation-only.yml
kubectl apply -f subsessions/04-vpa-recommendations/04-vpa-load-generator.yml
```

Check VPA recommendations:

```bash
kubectl describe vpa vpa-demo -n app-autoscaling
```

Optional, apply recommendations by recreating Pods:

```bash
kubectl apply -f subsessions/04-vpa-recommendations/03-vpa-auto-recreate.yml
kubectl delete pod -n app-autoscaling -l app=vpa-demo
kubectl get pods -n app-autoscaling -w
```

Run the memory HPA lab:

```bash
kubectl apply -f subsessions/06-memory-hpa/
```

Run the custom and external metrics HPA lab only after the metrics adapter or
provider-specific metric source is available:

```bash
kubectl apply -f subsessions/07-custom-external-metrics-hpa/01-custom-metric-demo.yml
```

## Cleanup

From `sessions/12-pod-autoscaling`:

```bash
kubectl delete -f subsessions/04-vpa-recommendations/ --ignore-not-found
kubectl delete -f subsessions/07-custom-external-metrics-hpa/ --ignore-not-found
kubectl delete -f subsessions/06-memory-hpa/ --ignore-not-found
kubectl delete -f subsessions/02-hpa-cpu-autoscaling/ --ignore-not-found
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
```

If you installed VPA only for this lab, remove it by following:

```text
subsessions/03-vpa-installation/README.md
```

Do not remove Metrics Server if other labs, dashboards, HPA, or VPA examples still need it.

## Troubleshooting

If HPA shows `<unknown>`:

```bash
kubectl top pods -n app-autoscaling
kubectl describe hpa cpu-demo -n app-autoscaling
kubectl describe pod -n app-autoscaling -l app=cpu-demo
```

Common causes:

- Metrics Server is missing or unhealthy.
- The target Pods do not have CPU requests.
- The Pods are not Ready yet.
- The workload has not produced enough metrics yet.

If VPA has no recommendation:

```bash
kubectl get vpa -n app-autoscaling
kubectl describe vpa vpa-demo -n app-autoscaling
kubectl get pods -n kube-system | grep vpa
kubectl top pods -n app-autoscaling
```

Common causes:

- VPA is not installed.
- Metrics Server is not installed.
- The Pods have not run long enough.
- There is too little real resource usage for the recommender to learn from.

## Review Questions

1. What field does HPA change on a Deployment?
2. Why does CPU-based HPA need CPU requests?
3. What happens if a Pod requests `100m` CPU and uses `100m` CPU?
4. Why is HPA usually better for stateless web applications?
5. Why is VPA not built into Kubernetes by default?
6. What is the difference between VPA `Off` and `Recreate` modes?
7. Why can CPU-based HPA and CPU-changing VPA conflict on the same Deployment?
8. When would you use VPA only for recommendations?
9. What must happen at the node layer if HPA creates more Pods than the cluster can schedule?

## References

- Kubernetes HPA documentation: `https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/`
- Kubernetes HPA walkthrough: `https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/`
- Kubernetes VPA documentation: `https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/`
- VPA installation documentation: `https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/installation.md`
- Metrics Server documentation: `https://github.com/kubernetes-sigs/metrics-server`
