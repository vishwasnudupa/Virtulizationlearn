# Module 07: Advanced Monitoring with Helm

## 🎯 Objective
Deploy a comprehensive observability stack (Prometheus, Grafana, Loki, Alertmanager) using Helm. This module focuses on "Day 2" operations: custom dashboards, persistent storage, and log aggregation.

## � Observability Flow Diagram

```mermaid
graph LR
    subgraph Kubernetes Cluster
        App[Your Application]
        
        subgraph Collectors
            SM[ServiceMonitor]
            Promtail[Promtail (Logs)]
        end
        
        subgraph Storage_Analysis
            Prom[Prometheus Server]
            Loki[Loki (Log Store)]
        end
        
        subgraph Visualization_Alerting
            Grafana[Grafana UI]
            Alertmgr[Alertmanager]
        end
    end
    
    App -->|Metrics /metrics| Prom
    App -->|Logs stdout| Promtail
    Promtail -->|Push Logs| Loki
    
    Prom -->|Rules Check| Alertmgr
    Alertmgr -->|Notify| Slack/Email
    
    Grafana -->|Query| Prom
    Grafana -->|Query| Loki
    
    SM -.->|Configures| Prom
```

## 🔑 Key Concepts Explained

### 1. The Operator Pattern
Normally, managing a stateful application like Prometheus is hard (reloading config, managing storage).
*   **Prometheus Operator**: A piece of software that runs in your cluster and manages Prometheus for you.
*   **CRDs (Custom Resource Definitions)**: The Operator extends the Kubernetes API. It adds new object types like `ServiceMonitor` and `PrometheusRule`. You create these YAMLs, and the Operator sees them and automatically reconfigures Prometheus.

### 2. ServiceMonitor
This is the magic of the Operator. Instead of editing a central `prometheus.yml` file, you just drop a `ServiceMonitor` file next to your application.
*   *Logic*: "Hey Prometheus, look for any Service with the label `app: frontend` and scrape port `8080`."

### 3. Loki & Promtail
*   **Loki**: Think of it as "Prometheus for Logs". It doesn't index the *text* of your logs (which is expensive), only the *metadata* (labels). This makes it very cheap and fast.
*   **Promtail**: The agent running on every node. It reads the log files that Docker/Containerd writes to disk, tags them with Pod names, and ships them to Loki.

## 📂 Structure
```
module-07-helm-monitoring/
├── values-prometheus.yaml  # Overrides for kube-prometheus-stack (Storage, Retention)
├── values-loki.yaml        # Overrides for loki-stack (Retention, Indexing)
└── README.md               # This guide
```

## 🚀 Usage Guide

### 1. Setup Helm Repositories
Helm needs to know where to download the charts from.
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### 2. Install Prometheus Stack
This installs Prometheus, Alertmanager, Grafana, and the Operator.
```bash
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  -f values-prometheus.yaml
```

### 3. Install Loki Stack
This installs Loki and Promtail.
```bash
helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  -f values-loki.yaml
```

### 4. Access Grafana
Grafana is the UI where you see everything.
```bash
# 1. Get the admin password (it's generated automatically)
kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# 2. Forward the port to your local machine
kubectl port-forward --namespace monitoring svc/prometheus-grafana 3000:80
```
*   **URL**: http://localhost:3000
*   **User**: `admin`
*   **Password**: (The output from step 1)
