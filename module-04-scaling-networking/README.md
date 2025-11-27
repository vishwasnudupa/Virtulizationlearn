# Module 4: Networking, Scaling & Observability

## 🎯 Objective
In this module, we will expose our application to the outside world and make it elastic. You will learn:
1.  **Ingress**: Routing external traffic to internal services.
2.  **Horizontal Pod Autoscaler (HPA)**: Automatically adding pods when load increases.
3.  **Probes**: Liveness and Readiness checks (Self-healing).

## 🏗️ Architecture (Module 4)

```mermaid
graph LR
    User[User Browser] -- http://sentinel.local --> Ingress[Ingress Controller]
    Ingress -- / --> Dashboard[Dashboard Service]
    Ingress -- /api/logs --> Collector[Collector Service]
    
    subgraph Autoscaling Group
        Analyzer1[Analyzer Pod]
        Analyzer2[Analyzer Pod]
        Analyzer3[Analyzer Pod]
    end
    
    HPA[HPA Controller] -- Watches CPU --> Autoscaling Group
```

## 🔑 Key Concepts

### 1. Ingress (`ingress.yaml`)
A Service (`NodePort` or `LoadBalancer`) is one way to expose apps, but **Ingress** is smarter. It acts as a Layer 7 HTTP router.
- **Host-based routing**: `sentinel.local` -> Dashboard.
- **Path-based routing**: `/api/logs` -> Collector.

### 2. Horizontal Pod Autoscaler (`hpa.yaml`)
Why wake up at 3 AM to add servers? HPA watches metrics (like CPU) and scales your Deployment up or down automatically.
- **Target**: Maintain 50% CPU utilization.
- **Limits**: Min 1, Max 10 pods.

## 🛠️ Hands-On Guide

### Prerequisites
- **Ingress Controller**: You must enable it.
    - Minikube: `minikube addons enable ingress`
    - Docker Desktop: It comes with one, or you can install Nginx Ingress via Helm.
- **Metrics Server**: Required for HPA.
    - Minikube: `minikube addons enable metrics-server`

### 1. Build Dashboard Image
```bash
docker build -t sentinel-dashboard:v1 ./dashboard-ui
```

### 2. Deploy Dashboard & Ingress
```bash
kubectl apply -f k8s/dashboard.yaml
kubectl apply -f k8s/ingress.yaml
```

### 3. Configure DNS
Add `sentinel.local` to your hosts file pointing to your cluster IP.
- **Windows**: `C:\Windows\System32\drivers\etc\hosts`
- **Linux/Mac**: `/etc/hosts`
- **Entry**: `127.0.0.1 sentinel.local` (or `minikube ip` if using minikube)

### 4. Test Ingress
Open your browser to `http://sentinel.local`. You should see the dashboard showing the queue length!

### 5. Configure Autoscaling
First, we need to set resource requests on our analyzer deployment so HPA can calculate usage.
*Edit `../module-03-config-state/k8s/analyzer-deployment.yaml` to add resources:*
```yaml
    resources:
      requests:
        cpu: "100m"
      limits:
        cpu: "200m"
```
Apply the updated deployment:
```bash
kubectl apply -f ../module-03-config-state/k8s/analyzer-deployment.yaml
```
Apply the HPA:
```bash
kubectl apply -f k8s/hpa.yaml
```

### 6. Stress Test
Run the generator with a very low interval to flood the system:
```bash
kubectl run load-test --image=sentinel-generator:v1 --env="INTERVAL=0.01" --env="COLLECTOR_URL=http://collector-service/logs"
```
Watch the HPA scale up:
```bash
kubectl get hpa -w
```
*You will see the replica count increase as CPU load rises!*

## 🧹 Cleanup
```bash
kubectl delete -f k8s/
kubectl delete pod load-test
```

## ⚡ Module Cheatsheet
| Command | Description |
| :--- | :--- |
| `kubectl get ingress` | Show Ingress rules and the Address (IP) allocated. |
| `kubectl get hpa` | Show HorizontalPodAutoscalers, targets, and current CPU usage. |
| `kubectl top pods` | Show current CPU and Memory usage for pods (requires Metrics Server). |
| `kubectl describe hpa <name>` | Detailed status of autoscaling events (why did it scale up?). |
| `minikube addons enable ingress` | Enable the Nginx Ingress Controller on Minikube. |

### 💡 Pro Tip: Watching Changes
Add `-w` or `--watch` to any `get` command to see updates in real-time.
Example: `kubectl get hpa -w` (Press Ctrl+C to stop).

---
**Next Step:** In Module 5, we will package everything into a **Helm Chart** for easy enterprise deployment.
