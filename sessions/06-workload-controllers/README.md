# Session 06: Workload Controllers, DaemonSets, Jobs, And CronJobs

This session explains workload controllers beyond a single Pod: Deployments,
DaemonSets, Jobs, and CronJobs.

The main teaching idea is:

```text
Deployment = run a desired number of application Pods.
DaemonSet = run one Pod on every matching Node.
Job = run work until it completes successfully.
CronJob = create Jobs on a schedule.
```

They are not replacements for each other. They are commonly used together.

Example:

```text
Deployment:
  web app, API, worker, frontend

DaemonSet:
  log collector, monitoring agent, node exporter, CNI agent, storage agent
```

## Deployment Versus DaemonSet

| Topic | Deployment | DaemonSet |
| --- | --- | --- |
| Main goal | Keep a chosen number of app replicas running | Keep one Pod running on each matching Node |
| Pod count | Controlled by `spec.replicas` | Controlled by number of eligible Nodes |
| Scaling | `kubectl scale deployment ... --replicas=N` | Add/remove matching Nodes or change node matching rules |
| Scheduling | Scheduler can place Pods on any suitable Nodes | Controller ensures each matching Node gets a Pod |
| Common use | Stateless apps, APIs, web tiers, workers | Node agents, log collectors, monitoring, networking, storage |
| Controller chain | Deployment creates ReplicaSets, ReplicaSets create Pods | DaemonSet creates Pods directly |

## How DaemonSet Pod Count Works

If a cluster has three eligible Nodes, a DaemonSet creates three Pods:

```text
node-1 -> daemonset-pod-a
node-2 -> daemonset-pod-b
node-3 -> daemonset-pod-c
```

If one more eligible Node joins, Kubernetes creates one more DaemonSet Pod.

If a Node is removed, the matching DaemonSet Pod disappears with that Node.

DaemonSets can be limited to selected Nodes with:

- `nodeSelector`
- node affinity
- taints and tolerations

## Running Deployments And DaemonSets In Mix

A normal production cluster usually runs both:

```text
User traffic
  -> Service
    -> Deployment Pods

Every Node
  -> DaemonSet Pod for logs, metrics, networking, or security
```

Important selector rule:

```text
Deployment Pods and DaemonSet Pods should use different labels/selectors.
```

If two controllers share the same selector, ownership and troubleshooting become confusing.

## Sub-Session Order

Follow the sub-sessions in this order:

1. `subsessions/01-prerequisites-and-namespace`: create the lab Namespace.
2. `subsessions/02-daemonset-basics`: run one small agent Pod per Node.
3. `subsessions/03-deployment-and-daemonset-mix`: run a Deployment and DaemonSet together.
4. `subsessions/04-job-basics`: run one-time and parallel batch work.
5. `subsessions/05-cronjob-basics`: run scheduled batch work.

## Target Shape By The End

```text
daemonset-lab Namespace

mix-web Service
  -> mix-web Deployment
    -> 4 nginx Pods placed wherever the scheduler has capacity

mix-node-agent DaemonSet
  -> 1 agent Pod on each matching Node
```

On a two-node cluster, expect something like:

```text
mix-web Deployment:       4 Pods total
mix-node-agent DaemonSet: 2 Pods total
```

The exact Deployment Pod placement can vary. The DaemonSet placement should map to the Nodes.

## Full Apply Order

From `sessions/06-workload-controllers`:

```bash
kubectl apply -f subsessions/01-prerequisites-and-namespace/
kubectl apply -f subsessions/02-daemonset-basics/
kubectl apply -f subsessions/03-deployment-and-daemonset-mix/
kubectl apply -f subsessions/04-job-basics/
kubectl apply -f subsessions/05-cronjob-basics/
```

Check the result:

```bash
kubectl get deployments -n daemonset-lab
kubectl get daemonsets -n daemonset-lab
kubectl get jobs -n daemonset-lab
kubectl get cronjobs -n daemonset-lab
kubectl get pods -n daemonset-lab -o wide
```

Useful watch command:

```bash
kubectl get pods -n daemonset-lab -o wide -w
```

## Cleanup

From `sessions/06-workload-controllers`:

```bash
kubectl delete -f subsessions/03-deployment-and-daemonset-mix/ --ignore-not-found
kubectl delete -f subsessions/05-cronjob-basics/ --ignore-not-found
kubectl delete -f subsessions/04-job-basics/ --ignore-not-found
kubectl delete -f subsessions/02-daemonset-basics/ --ignore-not-found
kubectl delete -f subsessions/01-prerequisites-and-namespace/ --ignore-not-found
```

## Review Questions

1. What decides the number of Pods for a Deployment?
2. What decides the number of Pods for a DaemonSet?
3. Why is a DaemonSet useful for log collection?
4. What happens to a DaemonSet when a new Node joins the cluster?
5. Why should a Deployment and DaemonSet not share the same selector?
6. If a cluster has four eligible Nodes, how many Pods should one DaemonSet create?
7. Why is a Deployment better than a DaemonSet for a stateless web API?
8. What is the difference between a Job and a CronJob?

## References

- Kubernetes DaemonSet documentation: `https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/`
- Kubernetes Deployment documentation: `https://kubernetes.io/docs/concepts/workloads/controllers/deployment/`
- Kubernetes labels and selectors: `https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/`
