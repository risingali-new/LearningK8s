# Session 28: Cluster Operations

This session teaches how to run and maintain clusters over time.

## Sub-Session Order

1. `01-version-skew`: Kubernetes component compatibility.
2. `02-upgrades`: control plane, node groups, add-ons.
3. `03-node-drain`: cordon, drain, uncordon.
4. `04-backup-and-restore`: Velero and disaster recovery.
5. `05-etcd-concepts`: why state backup matters.
6. `06-maintenance-windows`: safe production changes.
7. `07-cost-and-capacity`: rightsizing and cleanup.

## Useful Commands

```bash
kubectl cordon <node-name>
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
kubectl uncordon <node-name>
kubectl get pdb -A
kubectl get nodes
```

## Review Questions

1. Why do node drains matter during upgrades?
2. What does a PDB protect during maintenance?
3. Why should backup restore be tested?
4. What is version skew?
