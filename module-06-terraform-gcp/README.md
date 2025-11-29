# Module 06: Infrastructure as Code with Terraform on GCP

## 🎯 Objective
Provision a production-ready Google Kubernetes Engine (GKE) cluster and supporting infrastructure using Terraform. This module demonstrates advanced IaC patterns including remote state management, modular architecture, and security best practices.

## 🏗️ Architecture Diagram

```mermaid
graph TD
    subgraph GCP_Project [GCP Project]
        subgraph VPC [VPC Network]
            NAT[Cloud NAT Gateway]
            subgraph Subnet [Private Subnet]
                GKE[GKE Cluster Control Plane]
                
                subgraph NodePools [Node Pools]
                    NP1[Primary Pool (Standard)]
                    NP2[Spot Pool (Preemptible)]
                end
            end
        end
        
        GCS[GCS Bucket (Terraform State)]
        IAM[IAM Service Accounts]
    end

    User[DevOps Engineer] -->|Terraform Apply| GCS
    User -->|kubectl| GKE
    NodePools -->|Outbound Traffic| NAT
    NodePools -->|Workload Identity| IAM
```

## 🔑 Key Concepts Explained

### 1. VPC-Native Cluster
In a VPC-native cluster, Pods are first-class citizens of the VPC network.
*   **Traditional**: Pods use an overlay network and are not directly routable from the VPC.
*   **VPC-Native**: Pods get real IP addresses from a secondary range in the subnet. This improves performance and allows direct access to other VPC resources (like Cloud SQL) without complex NAT/Proxying.

### 2. Workload Identity
This is the secure way to let your Pods access Google Cloud APIs (like reading from a Storage Bucket).
*   **Old Way**: Exporting a JSON key for a Service Account and mounting it as a Kubernetes Secret. (Insecure! Keys get leaked).
*   **Workload Identity**: Maps a Kubernetes ServiceAccount (KSA) to a Google ServiceAccount (GSA). The Pod automatically gets a short-lived token. No keys to manage!

### 3. Remote State Backend
Terraform needs to track what it created. It stores this in a "State File".
*   **Local State**: Stored on your laptop. Bad for teams (locks are missing, code is not shared).
*   **Remote State (GCS)**: Stored in a Google Cloud Storage bucket. This allows your team to share the state and prevents two people from applying changes at the same time (Locking).

## 📂 Structure
```
module-06-terraform-gcp/
├── main.tf             # Core resource definitions (VPC, GKE, Nodes)
├── variables.tf        # Input variables (Region, Cluster Name)
├── outputs.tf          # Output values (Connection strings)
├── provider.tf         # Configures the Google Provider & Backend
├── terraform.tfvars    # Your specific values (GitIgnored!)
└── modules/            # (Optional) Reusable sub-components
```

## 🚀 Usage Guide

### Prerequisites
1.  **Google Cloud SDK**: Installed and authenticated (`gcloud auth login`).
2.  **Terraform**: Installed (`terraform -v`).
3.  **A GCP Project**: Created in the console.

### Step-by-Step

1.  **Authenticate**:
    ```bash
    gcloud auth application-default login
    ```

2.  **Initialize**:
    Downloads the Google provider plugins and sets up the backend.
    ```bash
    terraform init
    ```

3.  **Plan**:
    See what Terraform *will* do without actually doing it.
    ```bash
    terraform plan -out=tfplan
    ```

4.  **Apply**:
    Create the infrastructure. This takes ~15 minutes for a GKE cluster.
    ```bash
    terraform apply tfplan
    ```

5.  **Connect**:
    Configure `kubectl` to talk to your new cluster.
    ```bash
    gcloud container clusters get-credentials $(terraform output -raw cluster_name) --region $(terraform output -raw region)
    ```
