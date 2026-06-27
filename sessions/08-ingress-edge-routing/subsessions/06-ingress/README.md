# Sub-Session 06: ALB Ingress

This sub-session creates one ALB-backed Ingress that routes traffic to multiple
internal Services.

## Routing

```text
/api/users -> user-service:5001
/api/apps  -> app-service:5002
/          -> frontend:80
```

The frontend and APIs are still `ClusterIP` Services. The AWS Load Balancer
Controller creates and manages the external ALB.

If you want to use another Ingress controller instead, use one of the optional
controller sub-sessions after this one, such as
`subsessions/07-optional-f5-nginx-ingress`,
`subsessions/08-optional-traefik-ingress`, or
`subsessions/09-optional-haproxy-ingress`.

## Install AWS Load Balancer Controller

Run these commands once per EKS cluster before applying the ALB Ingress.

Set the cluster values:

```bash
export CLUSTER_NAME=demo-batch16a
export AWS_REGION=us-east-2
export VPC_ID=$(aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --query "cluster.resourcesVpcConfig.vpcId" \
  --output text)
```

Associate an IAM OIDC provider with the cluster:

```bash
eksctl utils associate-iam-oidc-provider \
  --cluster "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --approve
```

Download and create the AWS Load Balancer Controller IAM policy:

```bash
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json

aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json
```

Create the controller ServiceAccount with the policy attached:

```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

eksctl create iamserviceaccount \
  --cluster "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --namespace kube-system \
  --name aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
```

Install the controller with Helm:

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --namespace kube-system \
  --set clusterName="$CLUSTER_NAME" \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region="$AWS_REGION" \
  --set vpcId="$VPC_ID"
```

Check the controller:

```bash
kubectl get deployment -n kube-system aws-load-balancer-controller
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
```

## Apply

From `sessions/08-ingress-edge-routing`:

```bash
kubectl apply -f subsessions/06-ingress/
```

## Check

```bash
kubectl get ingress -n app-ingress
kubectl describe ingress message-board-ingress -n app-ingress
```

Wait until an address appears:

```bash
kubectl get ingress message-board-ingress -n app-ingress
```

The `ADDRESS` value is the AWS ALB DNS name.

## Test

```bash
export APP_DNS=<ingress-address>

curl http://$APP_DNS/api/users
curl http://$APP_DNS/api/users/stats
curl http://$APP_DNS/api/apps
curl http://$APP_DNS/api/apps/stats
```

Open:

```text
http://<ingress-address>
```

If you own a custom domain, create a DNS record that points to the Ingress load balancer address.
