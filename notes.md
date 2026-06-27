```sh
eksctl create cluster --name demo-k8slearning  --region us-east-2 --nodegroup-name standard-workers --node-type t3.medium --nodes 2 --nodes-min 2 --nodes-max 3 --node-ami-family=AmazonLinux2023 --version 1.36

--version 1.36


eksctl create nodegroup --cluster demo-k8slearning-b16pk --region us-east-2 --name standard-workers-al2023 --node-type t3.medium --nodes 2 --nodes-min 2 --nodes-max 3 --node-ami-family AmazonLinux2023

eksctl delete nodegroup --cluster demo-k8slearning-b16pk --region us-east-2 --name standard-workers


aws eks --region us-east-2 update-kubeconfig --name demo-k8slearning

eksctl delete cluster --name demo-batch16a --region us-east-2


eksctl utils associate-iam-oidc-provider --cluster demo-k8slearning-b16a --region us-east-2 --approve
eksctl create iamserviceaccount --name ebs-csi-controller-sa --namespace kube-system --cluster demo-k8slearning-b16a --region us-east-2 --role-name AmazonEKS_EBS_CSI_DriverRole --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicyV2 --approve

eksctl create addon --name aws-ebs-csi-driver --cluster demo-k8slearning-b16a --region us-esat-2 --service-account-role-arn arn:aws:iam::$ACCOUNT_ID:role/AmazonEKS_EBS_CSI_DriverRole --force
```
