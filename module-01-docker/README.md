# Module 1: Containerization Foundations

## 🎯 Objective
In this first module, we will build the foundation of the **Sentinel Log Analysis System**. You will learn how to:
1.  Write a **Python FastAPI** microservice (`log-collector`).
2.  Create an optimized **Dockerfile** using **multi-stage builds**.
3.  Orchestrate multiple containers (Service + Database) using **Docker Compose**.

## 🏗️ Architecture (Module 1)
At this stage, our system is simple but functional. It runs entirely on your local machine.

```mermaid
graph LR
    User[User / Script] -- POST /logs --> Collector[Log Collector Container]
    Collector -- Push Log --> Redis[Redis Container]
```

- **Log Collector**: A REST API that accepts log entries.
- **Redis**: An in-memory data store acting as a temporary message queue.

## 🛠️ Hands-On Guide

### 1. The Application Code (`log-collector/`)
We have a simple Python application in `main.py`. It uses the `FastAPI` framework.
- **Key Concept**: **12-Factor App Config**. Notice how we don't hardcode the Redis address? We use `os.getenv`. This allows us to change the database location without changing the code—crucial for containerization.

### 2. The Dockerfile (`log-collector/Dockerfile`)
Open the `Dockerfile`. We use a **Multi-Stage Build**.
- **Builder Stage**: Installs dependencies. It might have compilers (gcc) and other heavy tools.
- **Runtime Stage**: Copies *only* the installed libraries from the builder. It stays light and secure.
- **Security**: We create a non-root user (`appuser`). Running as root inside a container is a security risk!

### 3. Orchestration with Docker Compose (`docker-compose.yaml`)
Instead of running `docker run` commands manually, we define our infrastructure as code.
- **Services**: We define `log-collector` and `redis-queue`.
- **Networking**: We create a bridge network `sentinel-net`. Docker's internal DNS allows `log-collector` to reach Redis simply by using the hostname `redis-queue`.

## 🚀 Running the Project

1.  **Build and Start**:
    ```bash
    docker-compose up --build
    ```
    *You will see logs indicating the build process, followed by the services starting up.*

2.  **Test the API** (Open a new terminal):
    ```bash
    # Send a test log
    curl -X POST http://localhost:8000/logs \
      -H "Content-Type: application/json" \
      -d '{"service_name": "payment-service", "level": "ERROR", "message": "Transaction failed"}'
    ```

3.  **Verify in Redis**:
    You can exec into the redis container to check the data:
    ```bash
    docker-compose exec redis-queue redis-cli lrange logs_queue 0 -1
    ```

4.  **Shutdown**:
    ```bash
    docker-compose down
    ```

## 🧠 Pro Tips
> **Why Multi-stage?**
> A standard Python image might be 1GB. A slim, multi-stage image can be <100MB. This means faster deployments, lower storage costs, and smaller attack surface.

> **Why Docker Compose?**
> It mimics a production environment (microservices talking to each other) on your laptop. It's the standard for local development.

## ⚡ Module Cheatsheet
| Command | Description |
| :--- | :--- |
| `docker-compose up --build` | Build images and start all services in the background (or foreground without `-d`). |
| `docker-compose down` | Stop and remove containers, networks, and volumes defined in `docker-compose.yaml`. |
| `docker-compose ps` | List the status of services managed by Compose. |
| `docker-compose exec <service> <cmd>` | Execute a command inside a running service container (e.g., `redis-cli`). |
| `docker build -t <name> .` | Build a Docker image from a Dockerfile in the current directory. |

---
**Next Step:** In Module 2, we will take these containers and deploy them to a **Kubernetes Cluster**, learning about Pods and Deployments.
