# Case Study 01: IAM User Access To One Namespace

## Scenario

A developer has an AWS IAM user and needs access to only one Kubernetes
Namespace in an EKS cluster. They should be able to work in `case-team-a`, but
they must not get cluster-admin access, node access, or access to other
Namespaces.

This is a common access request because the words sound simple: "Give this IAM
user the team namespace." The implementation crosses four systems:

- IAM user permissions.
- IAM role trust and permission policies.
- EKS access entries.
- Kubernetes RBAC.

## Target Outcome

The IAM user can:

- Assume a dedicated IAM Role.
- Authenticate to the EKS API as that role.
- Read and manage common workload objects in `case-team-a`.
- Read Pod logs in `case-team-a`.

The IAM user cannot:

- Use Kubernetes before assuming the role.
- Access another Namespace such as `default`.
- Read cluster-scoped resources such as Nodes.
- Become `system:masters` or cluster-admin.

## Important Concept

An IAM user does not have a trust policy. A trust policy belongs to an IAM Role.
For this scenario, the IAM user gets permission to assume a role, and the role
trusts that exact user.

The two AWS-side checks are separate:

```text
IAM user identity policy
  -> allows sts:AssumeRole on the namespace access role

IAM role trust policy
  -> allows that exact IAM user to assume the role
```

After STS returns temporary role credentials, EKS authenticates the role and
Kubernetes RBAC authorizes the request.

## Request Flow

```text
IAM user access keys
  -> sts:AssumeRole
    -> temporary credentials for EksCaseTeamANamespaceRole
      -> aws eks get-token
        -> EKS access entry maps the role to group eks-case-team-a-developers
          -> Kubernetes RoleBinding grants that group a Role in case-team-a
            -> Kubernetes API allows or denies each request
```

## Objects Created

AWS objects:

```text
IAM Role: EksCaseTeamANamespaceRole
  trust policy:
    allows arn:aws:iam::<account-id>:user/<IAM_USER_NAME> to assume the role
  permission policy:
    allows eks:DescribeCluster for this cluster

IAM User inline policy:
  allows sts:AssumeRole on EksCaseTeamANamespaceRole

EKS access entry:
  principal: arn:aws:iam::<account-id>:role/EksCaseTeamANamespaceRole
  Kubernetes group: eks-case-team-a-developers
```

Kubernetes objects:

```text
Namespace: case-team-a

Deployment: namespace-access-demo
Service: namespace-access-demo

Role: namespace-developer
  namespace: case-team-a
  allows common workload operations in case-team-a

RoleBinding: team-a-developers-namespace-developer
  namespace: case-team-a
  subject group: eks-case-team-a-developers
```

## Prerequisites

You need:

- AWS CLI v2.
- `kubectl`.
- An existing EKS cluster.
- Admin access to create IAM objects, EKS access entries, and Kubernetes RBAC.
- One IAM user to receive namespace access.
- EKS access entries enabled on the cluster.

Check the cluster authentication mode:

```bash
aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --query 'cluster.accessConfig.authenticationMode' \
  --output text
```

The mode should be `API` or `API_AND_CONFIG_MAP`. If the cluster is still using
only `CONFIG_MAP`, enable access entries intentionally:

```bash
aws eks update-cluster-config \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --access-config authenticationMode=API_AND_CONFIG_MAP
```

Wait until the cluster update is complete before continuing.

## Set Lab Variables

Run from this case study folder:

```bash
cd sessions/31-case-studies/subsessions/01-iam-user-namespace-access
```

Set the lab values:

```bash
export CLUSTER_NAME=demo-batch16a
export AWS_REGION=us-east-2
export IAM_USER_NAME=replace-with-existing-iam-user

export NAMESPACE=case-team-a
export K8S_GROUP=eks-case-team-a-developers
export ROLE_NAME=EksCaseTeamANamespaceRole
```

## Step 1: Create The Namespace And RBAC

Apply the Kubernetes objects:

```bash
kubectl apply -f 01-namespace.yml
kubectl apply -f 02-namespace-rbac.yml
```

Check them:

```bash
kubectl get namespace case-team-a
kubectl get deployment,service -n case-team-a
kubectl describe role namespace-developer -n case-team-a
kubectl describe rolebinding team-a-developers-namespace-developer -n case-team-a
```

## Step 2: Create IAM Role, Policies, And EKS Access Entry

The `iam/` folder contains readable templates. The script below generates
filled JSON from your environment variables and applies it with the AWS CLI.

Run this as an AWS admin identity:

```bash
bash scripts/01-create-namespace-access.sh
```

This creates or updates:

- The IAM Role trust policy.
- The role permission policy for `eks:DescribeCluster`.
- The IAM user inline policy for `sts:AssumeRole`.
- The EKS access entry that maps the role to the Kubernetes group.

### Manual AWS CLI Path For Step 2

The script is useful for repeat runs, but do the first run manually so the IAM
and EKS boundary is clear. These are the exact AWS CLI calls, not another
helper script. If you use PowerShell, run each multi-line command on one line
or replace `\` with PowerShell line continuation.

In the examples below, replace these values before running the commands:

```text
111122223333      -> your AWS account ID
alice             -> the existing IAM user name
demo-batch16a     -> your EKS cluster name
us-east-2         -> your AWS region
```

First, discover the account and IAM user ARN:

```bash
aws sts get-caller-identity \
  --query Account \
  --output text

aws iam get-user \
  --user-name alice \
  --query 'User.Arn' \
  --output text
```

Create a file named `role-trust-policy.manual.json`. This policy says which
human IAM user is allowed to assume the namespace access role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificIamUserToAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:user/alice"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Create the IAM Role:

```bash
aws iam create-role \
  --role-name EksCaseTeamANamespaceRole \
  --assume-role-policy-document file://role-trust-policy.manual.json \
  --description "Namespace access role for case-team-a in demo-batch16a"
```

If the role already exists, update only the trust policy:

```bash
aws iam update-assume-role-policy \
  --role-name EksCaseTeamANamespaceRole \
  --policy-document file://role-trust-policy.manual.json
```

Create a file named `role-describe-cluster-policy.manual.json`. This lets the
assumed role discover only this EKS cluster endpoint and certificate authority:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowDescribeOnlyThisEksCluster",
      "Effect": "Allow",
      "Action": "eks:DescribeCluster",
      "Resource": "arn:aws:eks:us-east-2:111122223333:cluster/demo-batch16a"
    }
  ]
}
```

Attach that permission as an inline role policy:

```bash
aws iam put-role-policy \
  --role-name EksCaseTeamANamespaceRole \
  --policy-name EKSDescribeClusterForKubectl \
  --policy-document file://role-describe-cluster-policy.manual.json
```

Create a file named `user-assume-role-policy.manual.json`. This gives the IAM
user permission to request the role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAssumeNamespaceAccessRole",
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::111122223333:role/EksCaseTeamANamespaceRole"
    }
  ]
}
```

Attach that permission to the IAM user:

```bash
aws iam put-user-policy \
  --user-name alice \
  --policy-name AllowAssumeEksCaseTeamANamespaceRole \
  --policy-document file://user-assume-role-policy.manual.json
```

Create the EKS access entry. This is where the AWS role becomes a Kubernetes
principal with the group `eks-case-team-a-developers`:

```bash
aws eks create-access-entry \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --principal-arn arn:aws:iam::111122223333:role/EksCaseTeamANamespaceRole \
  --type STANDARD \
  --kubernetes-groups eks-case-team-a-developers
```

If the access entry already exists, update the Kubernetes group mapping:

```bash
aws eks update-access-entry \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --principal-arn arn:aws:iam::111122223333:role/EksCaseTeamANamespaceRole \
  --kubernetes-groups eks-case-team-a-developers
```

Verify what EKS has stored:

```bash
aws eks describe-access-entry \
  --cluster-name demo-batch16a \
  --region us-east-2 \
  --principal-arn arn:aws:iam::111122223333:role/EksCaseTeamANamespaceRole \
  --query 'accessEntry.{principalArn:principalArn,kubernetesGroups:kubernetesGroups}' \
  --output table
```

## Step 3: Prove The RBAC Shape Before The User Logs In

As the cluster admin, impersonate the Kubernetes group that the access entry
will provide:

```bash
kubectl auth can-i list pods \
  -n case-team-a \
  --as=case-study-check \
  --as-group=eks-case-team-a-developers

kubectl auth can-i patch deployments.apps \
  -n case-team-a \
  --as=case-study-check \
  --as-group=eks-case-team-a-developers

kubectl auth can-i list pods \
  -n default \
  --as=case-study-check \
  --as-group=eks-case-team-a-developers

kubectl auth can-i list nodes \
  --as=case-study-check \
  --as-group=eks-case-team-a-developers
```

Expected answers:

```text
yes
yes
no
no
```

## Step 4: Test With The IAM User

Now use the IAM user's AWS credentials. The helper script assumes the namespace
role, updates a kubeconfig context with the temporary credentials, then runs
allowed and denied checks.

Run this as the IAM user:

```bash
bash scripts/02-test-namespace-access.sh
```

Expected behavior:

```text
kubectl get pods -n case-team-a
  -> succeeds

kubectl auth can-i patch deployments.apps -n case-team-a
  -> yes

kubectl auth can-i list pods -n default
  -> no

kubectl auth can-i list nodes
  -> no
```

Manual AWS CLI path without the test script:

1. Configure the IAM user's normal access keys in a source profile:

```bash
aws configure --profile base-iam-user
```

2. Configure a second profile that assumes the namespace role:

```bash
aws configure set profile.team-a-namespace.role_arn \
  arn:aws:iam::111122223333:role/EksCaseTeamANamespaceRole

aws configure set profile.team-a-namespace.source_profile base-iam-user

aws configure set profile.team-a-namespace.region us-east-2
```

3. Confirm that the profile resolves to the role, not the IAM user:

```bash
aws sts get-caller-identity --profile team-a-namespace
```

4. Build a kubeconfig context that uses that profile:

```bash
aws eks update-kubeconfig \
  --name demo-batch16a \
  --region us-east-2 \
  --alias demo-batch16a-team-a \
  --profile team-a-namespace
```

5. Run the same allow and deny checks manually:

```bash
kubectl --context demo-batch16a-team-a get pods -n case-team-a
kubectl --context demo-batch16a-team-a auth can-i patch deployments.apps -n case-team-a
kubectl --context demo-batch16a-team-a auth can-i list pods -n default
kubectl --context demo-batch16a-team-a auth can-i list nodes
```

For day-to-day use, configure an AWS profile that assumes the role:

```text
[profile team-a-namespace]
role_arn = arn:aws:iam::<account-id>:role/EksCaseTeamANamespaceRole
source_profile = base-iam-user
region = us-east-2
```

Then use that profile when running `kubectl`:

```bash
export AWS_PROFILE=team-a-namespace
aws eks update-kubeconfig \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --alias "$CLUSTER_NAME-team-a"

kubectl get pods -n case-team-a
```

## How The Pieces Work Together

The IAM user policy answers this AWS question:

```text
Is this user allowed to call sts:AssumeRole for the namespace role?
```

The IAM role trust policy answers this AWS question:

```text
Does this role trust that user as a principal?
```

The role permission policy answers this AWS question:

```text
Can the assumed role call eks:DescribeCluster so kubectl can discover the
cluster endpoint and certificate authority?
```

The EKS access entry answers this EKS authentication question:

```text
When this IAM role calls the Kubernetes API, which Kubernetes username and
groups should EKS attach to the request?
```

The Kubernetes RoleBinding answers this Kubernetes authorization question:

```text
Does the group eks-case-team-a-developers have a Role in this Namespace that
allows the requested verb and resource?
```

## Common Mistakes

- Mapping the IAM user directly instead of mapping an assumable role. For a lab
  it can work, but the role pattern is easier to revoke, rotate, and reuse.
- Granting `system:masters`. That bypasses the namespace boundary.
- Creating a ClusterRoleBinding when a RoleBinding is enough.
- Forgetting that a RoleBinding is namespaced. Binding the same group in
  another Namespace grants access there too.
- Expecting IAM permissions to grant Kubernetes access. IAM authenticates the
  principal; Kubernetes RBAC authorizes Kubernetes resources.
- Forgetting that `roleRef` in a RoleBinding is immutable. Delete and recreate
  the RoleBinding if the referenced Role is wrong.

## Cleanup

Run this as the AWS admin identity:

```bash
bash scripts/03-cleanup-namespace-access.sh
```

Or remove the pieces manually:

```bash
kubectl delete -f 02-namespace-rbac.yml --ignore-not-found
kubectl delete -f 01-namespace.yml --ignore-not-found

aws eks delete-access-entry \
  --cluster-name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --principal-arn "arn:aws:iam::<account-id>:role/$ROLE_NAME"

aws iam delete-user-policy \
  --user-name "$IAM_USER_NAME" \
  --policy-name "AllowAssume${ROLE_NAME}"

aws iam delete-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name EKSDescribeClusterForKubectl

aws iam delete-role --role-name "$ROLE_NAME"
```

## References

- Amazon EKS access entries: `https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html`
- Amazon EKS creating access entries: `https://docs.aws.amazon.com/eks/latest/userguide/creating-access-entries.html`
- AWS IAM roles: `https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html`
- AWS IAM policies: `https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html`
- Kubernetes RBAC: `https://kubernetes.io/docs/reference/access-authn-authz/rbac/`
