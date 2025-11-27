# ☸️ Kubernetes: The Orchestration Module
### *Deep Dive into K8s Objects and Operations*

## 1. Workload Resources
Not everything is a "Deployment". K8s has specialized controllers for different needs.

*   **Deployment**: For stateless apps (Web Servers, APIs). Manages ReplicaSets. Supports rolling updates.
*   **StatefulSet**: For stateful apps (Databases).
    *   *Features*: Stable network IDs (`web-0`, `web-1`), ordered deployment/scaling, stable storage.
*   **DaemonSet**: Runs one copy of a Pod on *every* Node.
    *   *Use Case*: Log collectors (Fluentd), Monitoring agents (Prometheus Node Exporter).
*   **Job**: Runs a pod to completion (once).
    *   *Use Case*: Database migrations, batch processing.
*   **CronJob**: Runs a Job on a schedule.
    *   *Use Case*: Daily backups, report generation.

## 2. Service Types (Networking)
How do we expose Pods to the network?

*   **ClusterIP (Default)**: Internal IP only. Accessible within the cluster.
*   **NodePort**: Opens a specific port (e.g., 30007) on *every* Node's IP. External traffic can hit `NodeIP:NodePort`.
*   **LoadBalancer**: Asks the Cloud Provider (AWS/GCP) to provision a physical Load Balancer that points to the Service.
*   **ExternalName**: Maps a Service to a DNS name (e.g., `db.aws.com`).

## 3. Storage Architecture
*   **PersistentVolume (PV)**: A piece of storage in the cluster (like a hard drive). Admin provisions this.
*   **PersistentVolumeClaim (PVC)**: A request for storage by a user. "I need 10GB of ReadWriteOnce".
*   **StorageClass**: Defines "Classes" of storage (e.g., "fast-ssd", "cheap-hdd"). Allows dynamic provisioning (K8s creates the PV automatically when you make a PVC).

## 4. Security & RBAC
**Role-Based Access Control (RBAC)** controls who can do what.
*   **Role**: Defines permissions (e.g., "Can read Pods") within a *Namespace*.
*   **ClusterRole**: Defines permissions across the *entire Cluster*.
*   **ServiceAccount**: Identity for processes running in Pods.
*   **RoleBinding**: Connects a User/ServiceAccount to a Role.

## 🎓 The Master Command Reference

### 🔍 Context & Config
| Command | Description |
| :--- | :--- |
| `kubectl config get-contexts` | List available clusters. |
| `kubectl config use-context <name>` | Switch active cluster. |
| `kubectl config set-context --current --namespace=dev` | Set default namespace to 'dev'. |

### 📦 Pods & Debugging
| Command | Description |
| :--- | :--- |
| `kubectl get pods -o wide` | Show extra info (IP, Node). |
| `kubectl get pods --show-labels` | Show labels attached to pods. |
| `kubectl logs <pod> -c <container>` | Get logs of specific container in multi-container pod. |
| `kubectl logs <pod> --previous` | Get logs of the *crashed* instance. |
| `kubectl port-forward <pod> 8080:80` | Forward local port 8080 to pod port 80. |
| `kubectl top pod` | Show CPU/Memory usage (requires metrics-server). |

### 🛠️ Creating & Editing
| Command | Description |
| :--- | :--- |
| `kubectl create deployment web --image=nginx` | Quick deployment creation. |
| `kubectl expose deployment web --port=80` | Create a Service for a deployment. |
| `kubectl edit deployment web` | Open the YAML in default editor (Vi/Nano). |
| `kubectl scale deployment web --replicas=0` | Quick way to kill all pods. |

### 🧹 Housekeeping
| Command | Description |
| :--- | :--- |
| `kubectl delete pod <name> --grace-period=0 --force` | Force delete a stuck pod. |
| `kubectl api-resources` | List all available resource types in the cluster. |
| `kubectl explain deployment.spec` | Built-in documentation for YAML fields. |

### 🧠 Advanced JSONPath Tricks
| Command | Description |
| :--- | :--- |
| `kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'` | Get all external IPs. |
| `kubectl get pods --sort-by='.status.startTime'` | List pods sorted by age. |
