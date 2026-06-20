#!/bin/bash

clear

echo "========================================"
echo "      EKS Cluster Management Tool"
echo "========================================"
echo ""

# Check AWS CLI

if ! command -v aws &> /dev/null
then
echo "[ERROR] AWS CLI is not installed."
exit 1
fi

# Check eksctl

if ! command -v eksctl &> /dev/null
then
echo "[ERROR] eksctl is not installed."
exit 1
fi

# Check kubectl

if ! command -v kubectl &> /dev/null
then
echo "[ERROR] kubectl is not installed."
exit 1
fi

echo "AWS Identity"
echo "------------"
aws sts get-caller-identity

echo ""
echo "Configured AWS Region"
echo "---------------------"
aws configure get region

echo ""
echo "========================================"
echo "1. Create EKS Cluster"
echo "2. Delete EKS Cluster"
echo "3. Exit"
echo "========================================"
echo ""

read -p "Select option (1-3): " OPTION

####################################################

# CREATE CLUSTER

####################################################

if [ "$OPTION" = "1" ]; then

echo ""
echo "Cluster Creation Wizard"
echo "======================="
echo ""

read -p "Cluster Name: " CLUSTER_NAME

read -p "AWS Region (ap-south-1): " REGION

read -p "Kubernetes Version (example: 1.33): " K8S_VERSION

echo "DEBUG: Reached node selection section"

echo ""
echo "Available Node Types"
echo "===================="
echo "1. t3.small"
echo "2. t3.medium"
echo "3. t3.large"
echo ""

read -p "Select Node Type (1-3): " NODE_OPTION

case $NODE_OPTION in
    1) NODE_TYPE="t3.small" ;;
    2) NODE_TYPE="t3.medium" ;;
    3) NODE_TYPE="t3.large" ;;
    *) cho "Invalid selection"
        exit 1
        ;;
esac

read -p "Number of Nodes: " NODE_COUNT

echo ""
echo "========================================"
echo "Cluster Name : $CLUSTER_NAME"
echo "Region       : $REGION"
echo "Version      : $K8S_VERSION"
echo "Node Type    : $NODE_TYPE"
echo "Node Count   : $NODE_COUNT"
echo "========================================"
echo ""

read -p "Proceed with creation? (yes/no): " CONFIRM

if [ "$CONFIRM" = "yes" ]; then

    eksctl create cluster \
    --name $CLUSTER_NAME \
    --region $REGION \
    --version $K8S_VERSION \
    --nodegroup-name workers \
    --node-type $NODE_TYPE \
    --nodes $NODE_COUNT

    echo ""
    echo "Updating kubeconfig..."

    aws eks update-kubeconfig \
    --name $CLUSTER_NAME \
    --region $REGION

    echo ""
    echo "Cluster Nodes"
    echo "-------------"

    kubectl get nodes

    echo ""
    echo "[SUCCESS] Cluster Created Successfully"

else

    echo "Cluster creation cancelled."

fi

####################################################

# DELETE CLUSTER

####################################################

elif [ "$OPTION" = "2" ]; then

    echo ""
    echo "Available EKS Clusters"
    echo "======================"

    mapfile -t CLUSTERS < <(
        aws eks list-clusters \
        --region $(aws configure get region) \
        --query "clusters[]" \
        --output text | tr '\t' '\n'
    )

    if [ ${#CLUSTERS[@]} -eq 0 ]; then
        echo "No EKS clusters found."
        exit 0
    fi

    for i in "${!CLUSTERS[@]}"
    do
        echo "$((i+1)). ${CLUSTERS[$i]}"
    done

    echo ""

    read -p "Select Cluster Number: " CHOICE

    CLUSTER_NAME=$(echo "${CLUSTERS[$((CHOICE-1))]}" | xargs)

    if [ -z "$CLUSTER_NAME" ]; then
        echo "Invalid selection."
        exit 1
    fi

    REGION=$(aws configure get region)

    echo ""
    echo "Selected Cluster : $CLUSTER_NAME"
    echo "Region           : $REGION"
    echo ""

    read -p "Type DELETE to confirm: " CONFIRM

    if [ "$CONFIRM" = "DELETE" ]; then
    echo "DEBUG:"
    echo "[$CLUSTER_NAME]"

        eksctl delete cluster \
            --name "$CLUSTER_NAME" \
            --region "$REGION"

    else

        echo "Deletion cancelled."

    fi
fi