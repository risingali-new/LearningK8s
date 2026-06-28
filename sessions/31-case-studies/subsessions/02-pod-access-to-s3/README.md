# Case Study 02: Pod Access To S3

## Scenario

An application running in EKS needs to read and write objects in an S3 bucket.
The team asks, "Can we give the user's AWS permissions to the Pod?"

The production answer should be: no, do not give human user credentials to the
Pod. A Pod should receive its own workload identity with only the AWS
permissions that workload needs.

This case study uses EKS Pod Identity for the main lab. IRSA is still common
and valid, but Pod Identity is the simpler default pattern for new EKS
workloads because the association is managed through EKS instead of an OIDC
trust policy annotation on the ServiceAccount.

## Target Outcome

The Pod can:

- Run with a dedicated Kubernetes ServiceAccount.
- Receive temporary AWS credentials for one IAM Role.
- Call `sts:GetCallerIdentity` to prove which role it is using.
- Write and read objects under one S3 prefix.
- List only the allowed S3 prefix.

The Pod cannot:

- Use a human IAM user's long-lived access keys.
- Access every bucket in the AWS account.
- Use the worker node IAM role as an application permission bucket.
- Read or write outside the intended S3 prefix.

## Important Concept

Kubernetes RBAC and AWS IAM solve different authorization problems.

```text
Kubernetes RBAC
  -> controls what the Pod can do against the Kubernetes API

AWS IAM
  -> controls what the Pod can do against AWS APIs such as S3
```

A ServiceAccount by itself does not grant S3 access. The ServiceAccount becomes
useful for AWS only when EKS associates it with an IAM Role.

## Request Flow

```text
Pod starts with serviceAccountName: s3-client
  -> EKS Pod Identity Agent detects the Pod Identity association
    -> EKS Auth service calls STS for the associated IAM Role
      -> temporary AWS credentials are exposed to the Pod
        -> AWS SDK or AWS CLI calls S3 with those temporary credentials
          -> IAM policy allows or denies each S3 action and resource
```

## Objects Created

AWS objects:

```text
IAM Role: EksPodS3CaseStudyRole
  trust policy:
    trusts pods.eks.amazonaws.com
    allows sts:AssumeRole and sts:TagSession
    restricts session tags to the intended cluster, namespace, and ServiceAccount

IAM Role inline policy: S3CaseStudyBucketAccess
  allows s3:ListBucket for one prefix
  allows s3:GetObject and s3:PutObject for objects under that prefix

EKS Pod Identity Association:
  namespace: case-s3-access
  serviceAccount: s3-client
  roleArn: arn:aws:iam::<account-id>:role/EksPodS3CaseStudyRole
```

Kubernetes objects:

```text
Namespace: case-s3-access
ServiceAccount: s3-client
Job: s3-access-check
```

## Prerequisites

You need:

- AWS CLI v2.
- `kubectl`.
- An existing EKS cluster.
- Admin access to create IAM roles, IAM policies, EKS add-ons, and Pod Identity
  associations.
- An existing S3 bucket for the lab.
- Permission to put and read test objects in that bucket.

This lab writes only under this prefix:

```text
pod-identity-check/*
```

## Set Lab Variables

Run from this case study folder:

```bash
cd sessions/31-case-studies/subsessions/02-pod-access-to-s3
```

Set the lab values:

```bash
export CLUSTER_NAME=demo-batch16a
export AWS_REGION=us-east-2
export S3_BUCKET=replace-with-existing-bucket-name

export NAMESPACE=case-s3-access
export SERVICE_ACCOUNT=s3-client
export ROLE_NAME=EksPodS3CaseStudyRole
export S3_PREFIX=pod-identity-check
```

## Step 1: Create The Kubernetes Identity

Apply the Namespace and ServiceAccount:

```bash
kubectl apply -f 01-namespace-and-serviceaccount.yml
```

Check them:

```bash
kubectl get namespace case-s3-access
kubectl get serviceaccount s3-client -n case-s3-access
```

At this point the ServiceAccount still has no AWS permissions. It is only a
Kubernetes identity.

## Step 2: Create The IAM Role, S3 Policy, And Pod Identity Association

Run this as an AWS and Kubernetes admin identity:

```bash
bash scripts/01-create-s3-pod-identity.sh
```

This script:

- Verifies the S3 bucket is reachable.
- Installs the `eks-pod-identity-agent` EKS add-on if it is missing.
- Creates or updates the IAM Role trust policy.
- Creates or updates the S3 least-privilege IAM policy on the role.
- Creates or updates the EKS Pod Identity association.
- Applies the Namespace and ServiceAccount manifest.

### Manual AWS CLI Path For Step 2

The script is the repeatable path. For learning, run the AWS CLI commands one
by one. These are the exact AWS CLI calls, not another helper script. If you
use PowerShell, run each multi-line command on one line or replace `\` with
PowerShell line continuation.

In the examples below, replace these values before running the commands:

```text
111122223333          -> your AWS account ID
demo-batch16a         -> your EKS cluster name
us-east-2             -> your AWS region
my-training-bucket    -> your existing S3 bucket
```

First, discover the account ID and check that the bucket exists:

```bash
aws sts get-caller-identity \
  --query Account \
  --output text

aws s3api head-bucket \
  --bucket my-training-bucket
```

Make sure the Kubernetes identity exists:

```bash
kubectl apply -f 01-namespace-and-serviceaccount.yml
kubectl get serviceaccount s3-client -n case-s3-access
```

Check whether the EKS Pod Identity Agent add-on is already installed:

```bash
aws eks describe-addon \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --addon-name eks-pod-identity-agent
```

If the add-on does not exist, create it and wait for it to become active:

```bash
aws eks create-addon \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --addon-name eks-pod-identity-agent

aws eks wait addon-active \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --addon-name eks-pod-identity-agent
```

Create a file named `pod-identity-trust-policy.manual.json`. This policy says
that the EKS Pod Identity service may assume the role only for this cluster,
Namespace, and ServiceAccount:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowEksPodIdentityForSpecificWorkload",
      "Effect": "Allow",
      "Principal": {
        "Service": "pods.eks.amazonaws.com"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestTag/eks-cluster-name": "demo-batch16a",
          "aws:RequestTag/kubernetes-namespace": "case-s3-access",
          "aws:RequestTag/kubernetes-service-account": "s3-client"
        }
      }
    }
  ]
}
```

Create the IAM Role:

```bash
aws iam create-role \
  --role-name EksPodS3CaseStudyRole \
  --assume-role-policy-document file://pod-identity-trust-policy.manual.json \
  --description "Case study role for EKS Pod access to S3 prefix"
```

If the role already exists, update only the trust policy:

```bash
aws iam update-assume-role-policy \
  --role-name EksPodS3CaseStudyRole \
  --policy-document file://pod-identity-trust-policy.manual.json
```

Create a file named `s3-prefix-access-policy.manual.json`. This is the
least-privilege S3 policy for one bucket prefix:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListOnlyTheApplicationPrefix",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-training-bucket",
      "Condition": {
        "StringLike": {
          "s3:prefix": [
            "pod-identity-check",
            "pod-identity-check/*"
          ]
        }
      }
    },
    {
      "Sid": "ReadWriteOnlyTheApplicationPrefix",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-training-bucket/pod-identity-check/*"
    }
  ]
}
```

Attach the policy to the role:

```bash
aws iam put-role-policy \
  --role-name EksPodS3CaseStudyRole \
  --policy-name S3CaseStudyBucketAccess \
  --policy-document file://s3-prefix-access-policy.manual.json
```

Create the Pod Identity association. This is the EKS-side link between the
Kubernetes ServiceAccount and the IAM Role:

```bash
aws eks create-pod-identity-association \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --namespace case-s3-access \
  --service-account s3-client \
  --role-arn arn:aws:iam::111122223333:role/EksPodS3CaseStudyRole
```

If the association already exists, list it and update the role ARN:

```bash
aws eks list-pod-identity-associations \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --namespace case-s3-access \
  --service-account s3-client

aws eks update-pod-identity-association \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --association-id a-replace-with-association-id \
  --role-arn arn:aws:iam::111122223333:role/EksPodS3CaseStudyRole
```

Verify the association:

```bash
aws eks describe-pod-identity-association \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --association-id a-replace-with-association-id \
  --query 'association.{namespace:namespace,serviceAccount:serviceAccount,roleArn:roleArn}' \
  --output table
```

## Step 3: Run The Pod Access Check

Run the test Job:

```bash
bash scripts/02-run-s3-access-check.sh
```

Manual path without the helper script:

1. Create a local copy of `02-s3-access-check-job.yml`.
2. In the copy, replace `REPLACE_WITH_AWS_REGION` with your AWS region.
3. In the copy, replace `REPLACE_WITH_BUCKET_NAME` with your S3 bucket name.
4. If you changed the prefix, replace `pod-identity-check` with that prefix.
5. Apply, wait, and read the logs:

```bash
kubectl delete job s3-access-check \
  -n case-s3-access \
  --ignore-not-found

kubectl apply -f 02-s3-access-check-job.local.yml

kubectl wait \
  --for=condition=complete \
  job/s3-access-check \
  -n case-s3-access \
  --timeout=180s

kubectl logs job/s3-access-check -n case-s3-access
```

The Job uses the `s3-client` ServiceAccount and runs these checks from inside
the Pod:

```bash
aws sts get-caller-identity
aws s3 cp /tmp/check.txt "s3://$S3_BUCKET/$S3_PREFIX/<pod-name>.txt"
aws s3 ls "s3://$S3_BUCKET/$S3_PREFIX/"
aws s3 cp "s3://$S3_BUCKET/$S3_PREFIX/<pod-name>.txt" -
```

Expected behavior:

```text
sts:GetCallerIdentity
  -> shows the assumed EksPodS3CaseStudyRole

s3 put/list/get under pod-identity-check/
  -> succeeds
```

## Step 4: Prove The Permission Boundary

Run the deny-check Job:

```bash
bash scripts/03-run-s3-deny-check.sh
```

Manual path without the helper script:

1. Create a local copy of `03-s3-deny-check-job.yml`.
2. In the copy, replace `REPLACE_WITH_AWS_REGION` with your AWS region.
3. In the copy, replace `REPLACE_WITH_BUCKET_NAME` with your S3 bucket name.
4. Apply, wait, and read the logs:

```bash
kubectl delete job s3-deny-check \
  -n case-s3-access \
  --ignore-not-found

kubectl apply -f 03-s3-deny-check-job.local.yml

kubectl wait \
  --for=condition=complete \
  job/s3-deny-check \
  -n case-s3-access \
  --timeout=180s

kubectl logs job/s3-deny-check -n case-s3-access
```

The Job uses the same ServiceAccount, but tries to write outside the allowed
prefix:

```text
s3://<bucket>/not-allowed/<pod-name>.txt
```

The script expects the AWS CLI command inside the Pod to fail with
`AccessDenied`. The denial comes from AWS IAM, not Kubernetes RBAC. Kubernetes
allowed the Pod to run; IAM denied the S3 action because the object key was
outside the allowed prefix.

## How The Pieces Work Together

The ServiceAccount answers this Kubernetes question:

```text
Which workload identity is this Pod running as?
```

The Pod Identity association answers this EKS question:

```text
Which IAM Role should Pods using this ServiceAccount receive?
```

The IAM role trust policy answers this AWS question:

```text
Can the EKS Pod Identity service assume this role for this cluster, Namespace,
and ServiceAccount?
```

The IAM S3 policy answers this AWS question:

```text
Which bucket actions and object keys are allowed for the temporary credentials?
```

The S3 bucket policy, if your organization uses one, can add another boundary:

```text
Even if the role policy allows access, does the bucket policy also allow it?
```

## Production Guidance

- Do not bake AWS access keys into container images, ConfigMaps, Secrets, or
  environment variables for normal EKS workloads.
- Do not rely on the node IAM role for application S3 permissions. Every Pod on
  that node can become harder to reason about.
- Create one IAM Role per workload or per permission boundary.
- Scope S3 policies to the exact bucket and prefix the application needs.
- Avoid `s3:*` and `Resource: "*"`.
- Treat `s3:ListBucket` separately from object permissions. Listing a bucket
  uses the bucket ARN, while reading and writing objects uses object ARNs.
- Review CloudTrail for `AssumeRole` and S3 data events when auditing access.
- Rotate or remove the Pod Identity association when the workload is retired.

## Common Mistakes

- Giving the developer's IAM user access keys to the Pod.
- Annotating a ServiceAccount for IRSA and also creating a Pod Identity
  association without knowing which path the SDK will use.
- Forgetting to install the EKS Pod Identity Agent.
- Creating the IAM Role but forgetting the Pod Identity association.
- Allowing `s3:ListAllMyBuckets` when the app only needs one bucket prefix.
- Allowing all object keys with `arn:aws:s3:::bucket/*` when the app needs only
  one prefix.
- Forgetting that S3 bucket names are globally unique and do not include the AWS
  account ID in the ARN.

## Cleanup

Run this as the AWS and Kubernetes admin identity:

```bash
bash scripts/04-cleanup-s3-pod-identity.sh
```

The cleanup removes:

- The test Jobs.
- The Pod Identity association.
- The role inline policy.
- The IAM Role.
- The Namespace and ServiceAccount.

It does not delete the S3 bucket and does not uninstall the
`eks-pod-identity-agent` add-on, because other workloads may depend on them.

## References

- Amazon EKS Pod Identity: `https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html`
- EKS Pod Identity IAM role trust policy: `https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html`
- EKS Pod Identity association: `https://docs.aws.amazon.com/eks/latest/userguide/pod-id-association.html`
- Amazon S3 IAM policy actions: `https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-policy-actions.html`
- Amazon S3 bucket policies and user policies: `https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-policies-s3.html`
