# Sub-Session 05: StorageClass

This sub-session introduces dynamic storage provisioning with a StorageClass.

## Why StorageClass Is Used

Static PVs are useful for learning, but they do not scale well. In real clusters, users should be able to request storage and let Kubernetes create the backing disk automatically.

A StorageClass defines what kind of storage to create.

## How Kubernetes Uses It

With dynamic provisioning:

```text
PVC requests storage -> StorageClass calls CSI driver -> PV is created automatically
```

For EKS, this example uses the Amazon EBS CSI provisioner:

```text
ebs.csi.aws.com
```

## EKS Requirement

The Amazon EBS CSI driver must be installed in the cluster.

For a standard EKS cluster, first make sure the cluster has an IAM OIDC provider:

```bash
eksctl utils associate-iam-oidc-provider \
  --cluster demo-k8slearning-b16a \
  --region us-east-2 \
  --approve
```

Find the AWS-managed EBS CSI policy available in your account:

```bash
EBS_CSI_POLICY_ARN=$(aws iam list-policies \
  --scope AWS \
  --query "Policies[?PolicyName=='AmazonEBSCSIDriverPolicyV2'].Arn | [0]" \
  --output text)

if [ "$EBS_CSI_POLICY_ARN" = "None" ]; then
  EBS_CSI_POLICY_ARN=$(aws iam list-policies \
    --scope AWS \
    --query "Policies[?PolicyName=='AmazonEBSCSIDriverPolicy'].Arn | [0]" \
    --output text)
fi

echo "$EBS_CSI_POLICY_ARN"
```

Create the IAM role used by the EKS add-on:

```bash
eksctl create iamserviceaccount \
  --name ebs-csi-controller-sa \
  --namespace kube-system \
  --cluster demo-k8slearning-b16a \
  --region us-east-2 \
  --role-name AmazonEKS_EBS_CSI_DriverRole \
  --role-only \
  --attach-policy-arn "$EBS_CSI_POLICY_ARN" \
  --approve
```

If the CloudFormation stack fails, inspect the exact reason:

```bash
aws cloudformation describe-stack-events \
  --region us-east-2 \
  --stack-name eksctl-demo-k8slearning-b16a-addon-iamserviceaccount-kube-system-ebs-csi-controller-sa \
  --query "StackEvents[?ResourceStatus=='CREATE_FAILED'].[Timestamp,LogicalResourceId,ResourceStatusReason]" \
  --output table
```

If the stack failed because `AmazonEBSCSIDriverPolicyV2` does not exist, delete the failed stack and rerun the role creation with the policy ARN detected above.

Then install or update the EBS CSI add-on with the role ARN:

```bash
ROLE_ARN=$(aws iam get-role \
  --role-name AmazonEKS_EBS_CSI_DriverRole \
  --query "Role.Arn" \
  --output text)

aws eks create-addon \
  --cluster-name demo-k8slearning-b16a \
  --region us-east-2 \
  --addon-name aws-ebs-csi-driver \
  --service-account-role-arn "$ROLE_ARN"
```

Check:

```bash
kubectl get csidriver
kubectl get storageclass
```

## Manifest

```text
01-storageclass-aws-ebs-gp3.yml
```

It creates a gp3 EBS StorageClass named:

```text
ebs-gp3
```

## Apply

From `sessions/07-storage-pv-pvc-statefulset`:

```bash
kubectl apply -f subsessions/05-storageclass/
```

## Check

```bash
kubectl get storageclass
kubectl describe storageclass ebs-gp3
```

The next sub-session uses this StorageClass in a StatefulSet `volumeClaimTemplates`.
