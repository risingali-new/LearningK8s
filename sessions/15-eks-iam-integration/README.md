# Session 15: EKS IAM Integration

This session connects Kubernetes identities to AWS permissions.

## Sub-Session Order

1. `01-eks-authentication`: IAM authentication to the EKS API.
2. `02-aws-auth-and-access-entries`: cluster access mapping.
3. `03-irsa`: IAM Roles for Service Accounts.
4. `04-eks-pod-identity`: modern EKS Pod Identity flow.
5. `05-addon-permissions`: EBS CSI, AWS Load Balancer Controller, ExternalDNS.
6. `06-least-privilege`: scoping AWS permissions per workload.

## Lab Ideas

- Create an IAM role for a ServiceAccount.
- Deploy a Pod that calls AWS STS.
- Compare IRSA and EKS Pod Identity.
- Attach permissions for EBS CSI or AWS Load Balancer Controller.

## Review Questions

1. Why is Kubernetes RBAC not the same as AWS IAM?
2. What problem does IRSA solve?
3. What problem does EKS Pod Identity solve?
4. Why should AWS permissions be workload-specific?
