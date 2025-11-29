# The Ultimate Guide to Google Cloud Platform (GCP) for Kubernetes

## 1. Introduction to GCP
Google Cloud Platform (GCP) is a suite of cloud computing services that runs on the same infrastructure that Google uses internally. It is particularly known for its Kubernetes support, as Kubernetes was originally designed by Google.

---

## 2. Key Services for Kubernetes

### ☸️ Google Kubernetes Engine (GKE)
GKE is the managed Kubernetes service.
*   **Control Plane**: Managed by Google (you don't see the master nodes). High availability and upgrades are handled automatically.
*   **Node Pools**: Groups of worker nodes (VMs). You can have different pools for different workloads (e.g., GPU nodes for AI, High-Memory nodes for databases).
*   **Autopilot vs. Standard**:
    *   *Standard*: You manage the nodes and pay for the VMs.
    *   *Autopilot*: Google manages the nodes; you pay only for the Pod resources (CPU/RAM) you request.

### 🌐 Virtual Private Cloud (VPC)
The networking layer.
*   **Subnets**: GKE clusters run in subnets.
*   **VPC-Native Clusters**: Pods get their own IP addresses from the VPC, allowing them to communicate directly with other VPC resources (like Cloud SQL) without NAT.
*   **Cloud NAT**: Allows private nodes (nodes with no public IP) to access the internet (e.g., to pull Docker images) securely.

### 🛡️ Identity and Access Management (IAM)
*   **Service Accounts (SA)**: Special accounts for applications (not people).
*   **Workload Identity**: The modern, secure way to let GKE Pods access GCP services. It maps a Kubernetes ServiceAccount (KSA) to a Google ServiceAccount (GSA). This avoids storing secrets/keys inside the cluster.

### 💾 Storage
*   **Cloud Storage (GCS)**: Object storage (like S3). Used for storing Terraform state, backups, and static assets.
*   **Persistent Disk**: Block storage attached to nodes. GKE uses this for PersistentVolumes (PVs).

### 🗄️ Databases
*   **Cloud SQL**: Managed MySQL, PostgreSQL, and SQL Server.
*   **Firestore**: NoSQL document database.

---

## 3. GKE Networking Deep Dive

### Pod IP Ranges
In a VPC-native cluster, you define secondary IP ranges on your subnet:
1.  **Primary Range**: For Nodes.
2.  **Secondary Range 1**: For Pods.
3.  **Secondary Range 2**: For Services (ClusterIPs).

### Load Balancing
*   **L4 Load Balancer**: Created by a Kubernetes `Service` of type `LoadBalancer`. Handles TCP/UDP traffic.
*   **L7 Load Balancer (Ingress)**: Created by a Kubernetes `Ingress`. Handles HTTP/HTTPS, SSL termination, and path-based routing. GKE uses the Google Cloud Load Balancer (GCLB) for this.

---

## 4. Observability in GCP
*   **Cloud Logging**: Automatically collects stdout/stderr logs from all containers.
*   **Cloud Monitoring**: Collects metrics (CPU, Memory) from nodes and pods.

---

## 5. Cost Optimization Tips
1.  **Spot VMs (Preemptible)**: Use Spot instances for stateless workloads (like batch jobs or stateless web apps). They are up to 91% cheaper but can be reclaimed by Google at any time.
2.  **Cluster Autoscaler**: Automatically adds nodes when pods are pending and removes nodes when they are underutilized.
3.  **Horizontal Pod Autoscaler (HPA)**: Scales the number of Pods based on CPU/Memory usage.
