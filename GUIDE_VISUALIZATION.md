# 🗺️ Visualization: The Observability Module
### *Monitoring, Logging, and Tracing Strategies*

## 1. Observability Strategy
How do you decide what to monitor?

### 🔴 The RED Method (For Services)
Best for request-driven microservices.
1.  **Rate**: The number of requests per second.
2.  **Errors**: The number of failed requests.
3.  **Duration**: How long requests take (Latency).

### 🛠️ The USE Method (For Resources)
Best for infrastructure (Nodes, Disks, CPUs).
1.  **Utilization**: How busy is the resource? (e.g., CPU at 90%).
2.  **Saturation**: How much work is queued/waiting? (e.g., Disk I/O queue).
3.  **Errors**: Are there hardware/system errors?

## 2. The 3 Pillars (Deep Dive)

### 🪵 Logs (Structured vs Unstructured)
*   **Unstructured**: `User logged in`. Hard for machines to parse.
*   **Structured (JSON)**: `{"event": "login", "user_id": 123, "status": "success"}`.
    *   *Pro Tip*: Always log in JSON in production. It allows tools like Kibana/Loki to filter by field (e.g., `status="failed"`).

### 📈 Metrics (Types)
*   **Counter**: Only goes up (e.g., `http_requests_total`).
*   **Gauge**: Goes up and down (e.g., `memory_usage_bytes`).
*   **Histogram**: Tracks distribution (e.g., "99% of requests took < 200ms").

### 🕸️ Tracing (Context Propagation)
How does Jaeger know that *this* DB query belongs to *that* user click?
*   **Trace ID**: A unique ID generated at the edge (Load Balancer).
*   **Span ID**: A unique ID for each step.
*   **Propagation**: Headers (e.g., `x-b3-traceid`) are passed from service to service. If you drop the header, you break the trace.

## 3. Service Mesh (The Future of Observability)
Tools like **Istio** or **Linkerd**.
*   **Sidecar Pattern**: They inject a tiny proxy container next to *every* app container.
*   **Benefit**: The proxy automatically captures metrics (RED method) and traces without you changing a single line of code.

## 4. Alerting Philosophy
*   **Page on Symptoms, not Causes**.
    *   *Bad Alert*: "CPU is high". (Maybe the machine is just working hard? Is the user affected?)
    *   *Good Alert*: "Error Rate is > 1%". (Users are definitely failing).
*   **Alert Fatigue**: If you get 100 alerts a day, you will ignore the one real emergency.

## 🎓 The Master Tool Reference

### 📊 Grafana (Visualization)
*   **Data Sources**: Prometheus, Loki, InfluxDB, CloudWatch.
*   **Key Feature**: "Variables". Create a dropdown menu to switch between "Prod" and "Staging" on the same dashboard.

### 🤖 Prometheus (Metrics)
*   **PromQL Cheat Sheet**:
    *   `up`: Is the instance reachable? (1=Yes, 0=No).
    *   `rate(http_requests_total[5m])`: Per-second rate averaged over 5 mins.
    *   `sum(rate(http_requests_total[5m])) by (service)`: Total rate per service.
    *   `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`: The 95th percentile latency.

### 🔍 Loki (Logs)
*   **LogQL Cheat Sheet**:
    *   `{app="sentinel"}`: Select logs for app 'sentinel'.
    *   `{app="sentinel"} |= "error"`: Filter lines containing "error".
    *   `rate({app="sentinel"} |= "error" [5m])`: Calculate the rate of error logs per second! (Turning logs into metrics).
