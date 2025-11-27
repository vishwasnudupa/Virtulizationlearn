# 🐳 Docker: The Containerization Module
### *From Basics to Advanced Architecture*

## 1. Docker Architecture
Docker is a client-server application.
*   **Docker Daemon (`dockerd`)**: The background process that manages images, containers, and networks. It does the heavy lifting.
*   **Docker Client (`docker`)**: The CLI tool you use. It sends API requests to the Daemon.
*   **Docker Registry**: The remote storage for images (Docker Hub, ECR).

## 2. The Container Lifecycle
Understanding the state machine of a container is crucial.
1.  **Created**: The container is created but not started.
2.  **Running**: The process is active.
3.  **Paused**: The process is frozen (SIGSTOP).
4.  **Stopped**: The process has exited (SIGTERM/SIGKILL).
5.  **Deleted**: The container is removed from disk.

## 3. Data Persistence (Volumes)
Containers are **ephemeral**. If you delete a container, its filesystem is gone.
*   **Bind Mounts**: Maps a file/folder from your *Host Machine* into the container.
    *   *Use Case*: Live code reloading during development.
    *   *Flag*: `-v /path/on/host:/path/in/container`
*   **Volumes**: Managed by Docker. Stored in a special area of the host filesystem.
    *   *Use Case*: Database storage, persistent data.
    *   *Flag*: `-v volume_name:/path/in/container`

## 4. Networking
*   **Bridge (Default)**: Containers are on a private internal network. They can talk to each other if on the same bridge.
*   **Host**: The container shares the host's networking namespace. Port 80 in container = Port 80 on host. Fast, but insecure.
*   **None**: No networking.

## 5. Docker Compose
A tool for defining and running multi-container Docker applications.
*   **`docker-compose.yaml`**: The blueprint.
*   **Services**: The containers to run.
*   **Networks**: How they talk.
*   **Volumes**: Where they store data.

## 🎓 The Master Command Reference

### 🏗️ Build & Manage Images
| Command | Description |
| :--- | :--- |
| `docker build -t app:v1 .` | Build an image from Dockerfile in current dir. |
| `docker images` | List all local images. |
| `docker rmi <image_id>` | Delete an image. |
| `docker history <image_id>` | See the layers that make up an image. |
| `docker prune -a` | Delete all unused images (DANGEROUS). |

### 🏃 Run & Manage Containers
| Command | Description |
| :--- | :--- |
| `docker run -d -p 80:80 --name web app:v1` | Run detached (-d), map port (-p), name it (--name). |
| `docker ps -a` | List all containers (running and stopped). |
| `docker stop <name>` | Gracefully stop (SIGTERM). |
| `docker kill <name>` | Force stop (SIGKILL). |
| `docker rm <name>` | Remove a stopped container. |
| `docker rm -f <name>` | Force remove a running container. |

### 🕵️ Debugging & Inspection
| Command | Description |
| :--- | :--- |
| `docker logs -f <name>` | Follow (-f) the stdout/stderr logs. |
| `docker exec -it <name> /bin/bash` | Interactive shell inside the container. |
| `docker inspect <name>` | View detailed JSON metadata (IP, Volumes, Env). |
| `docker stats` | Live stream of CPU/RAM usage for all containers. |

### 🕸️ Networking & Volumes
| Command | Description |
| :--- | :--- |
| `docker network ls` | List networks. |
| `docker network create my-net` | Create a custom bridge network. |
| `docker volume create my-vol` | Create a named volume. |
| `docker volume inspect my-vol` | Find where the volume lives on disk. |

### 🐙 Docker Compose
| Command | Description |
| :--- | :--- |
| `docker-compose up -d` | Start all services in background. |
| `docker-compose down` | Stop and remove containers and networks. |
| `docker-compose logs -f` | Follow logs of all services. |
| `docker-compose build` | Rebuild services. |
