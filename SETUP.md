# 🛠️ Environment Setup Guide

It looks like you are having trouble running the commands. This guide will help you set up your Windows environment correctly.

## 1. Install Docker Desktop 🐳
You cannot run this project without Docker.
1.  **Download**: Go to [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/).
2.  **Install**: Run the installer. Ensure "Use WSL 2 instead of Hyper-V" is checked (recommended).
3.  **Start**: Open the "Docker Desktop" app from your Start Menu.
4.  **Verify**:
    Open a **new** PowerShell terminal and run:
    ```powershell
    docker --version
    ```
    *If you see an error like "The term 'docker' is not recognized", try restarting your computer or adding Docker to your PATH.*

## 2. Check Your PATH
If Docker is installed but not found:
1.  Search for **"Edit the system environment variables"** in Windows Search.
2.  Click **"Environment Variables"**.
3.  Under **"System variables"**, find `Path` and click **Edit**.
4.  Ensure `C:\Program Files\Docker\Docker\resources\bin` is in the list.

## 3. Python (Optional) 🐍
You received an error about Python. **You do NOT need Python installed** to run the Docker parts of this course.
*   **Recommendation**: Skip the `python -m venv` steps.
*   **If you really want to run Python locally**:
    1.  Install Python from the [Microsoft Store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K).
    2.  Restart PowerShell.

## 4. Running the Tests 🧪
Once Docker is working:
1.  Open PowerShell.
2.  Navigate to the module: `cd module-01-docker`
3.  Run the test: `.\test_module.ps1`

> **Note**: If `docker-compose` fails, try `docker compose` (with a space). The test script tries to handle both.
