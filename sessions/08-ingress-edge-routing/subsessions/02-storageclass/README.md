# Sub-Session 02: StorageClass

This sub-session creates the dynamic StorageClass used by the PostgreSQL StatefulSet.

The Amazon EBS CSI driver must already be installed. If it is not installed yet, follow the EBS CSI setup steps in:

```text
../../../07-storage-pv-pvc-statefulset/subsessions/05-storageclass/README.md
```

## Apply

From `sessions/08-ingress-edge-routing`:

```bash
kubectl apply -f subsessions/02-storageclass/
```

## Check

```bash
kubectl get storageclass ebs-gp3
```
