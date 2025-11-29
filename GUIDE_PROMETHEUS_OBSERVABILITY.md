# The Ultimate Guide to Observability: Prometheus & Grafana

## 1. What is Observability?
Observability is the ability to understand the internal state of a system by examining its outputs. In Kubernetes, this typically involves three pillars:
1.  **Metrics**: "What is happening?" (e.g., CPU usage is 80%).
2.  **Logs**: "Why is it happening?" (e.g., Error: Connection refused).
3.  **Traces**: "Where is it happening?" (e.g., Latency in the payment-service).

---

## 2. Prometheus: The Metrics Powerhouse
Prometheus is the standard for Kubernetes monitoring. It uses a **Pull Model**, meaning it periodically "scrapes" metrics from your applications.

### Architecture
*   **Prometheus Server**: The core. It scrapes targets, stores data in a Time Series Database (TSDB), and evaluates alerting rules.
*   **Exporters**: Small binaries that run alongside services to expose metrics.
    *   *Node Exporter*: Exposes hardware metrics (Disk, CPU, Network).
    *   *Kube-State-Metrics*: Exposes K8s object states (Pod status, Deployment replicas).
*   **Alertmanager**: Handles alerts sent by Prometheus. It groups, deduplicates, and routes them to receivers (Slack, PagerDuty, Email).
*   **Pushgateway**: For short-lived jobs that cannot be scraped (batch scripts).

### ServiceMonitors
The **Prometheus Operator** introduces a custom resource called `ServiceMonitor`. This tells Prometheus *what* to scrape. Instead of editing a huge config file, you just create a YAML file that says "Scrape any Service with the label `app: my-app`".

---

## 3. PromQL (Prometheus Query Language)
PromQL is used to query the data.
*   **Instant Vector**: Values at a single point in time.
    *   `http_requests_total`
*   **Range Vector**: Values over a time period.
    *   `http_requests_total[5m]`
*   **Rate**: Calculates the per-second rate of increase.
    *   `rate(http_requests_total[5m])` (Requests per second over the last 5 mins).

---

## 4. Grafana: The Visualization Layer
Prometheus collects data; Grafana makes it beautiful.
*   **Data Sources**: Grafana connects to Prometheus, Loki, CloudWatch, etc.
*   **Dashboards**: Collections of panels (graphs, gauges, tables).
*   **Variables**: Dropdown menus at the top of dashboards (e.g., select `namespace` or `pod`) to make dashboards dynamic.

---

## 5. Loki: Like Prometheus, but for Logs
Loki is a log aggregation system designed to be cost-effective.
*   **Index-Free**: Unlike Elasticsearch, Loki doesn't index the *content* of the logs, only the *labels* (metadata). This makes it extremely cheap and fast to write.
*   **Promtail**: The agent that runs on every node (DaemonSet). It reads log files from `/var/log/pods`, attaches labels (pod name, namespace), and pushes them to Loki.
*   **LogQL**: The query language for Loki, heavily inspired by PromQL.
    *   `{app="frontend"} |= "error"` (Show logs from frontend app containing "error").

---

## 6. The "Day 2" Monitoring Stack
A production-ready stack usually consists of:
1.  **Prometheus Operator**: Manages the lifecycle of Prometheus.
2.  **Kube-Prometheus-Stack**: A Helm chart that installs Prometheus, Grafana, Alertmanager, and default dashboards/alerts.
3.  **Loki-Stack**: Installs Loki and Promtail.
4.  **External-DNS / Ingress**: To expose the Grafana UI securely.
