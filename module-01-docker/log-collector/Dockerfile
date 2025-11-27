# ==========================================
# Stage 1: Builder
# ==========================================
# We use a larger image with build tools to install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies (if any were needed for C extensions)
# RUN apt-get update && apt-get install -y gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Runtime
# ==========================================
# We use a slim image for the final container to keep it small and secure
FROM python:3.11-slim as runtime

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local /usr/local

# Update PATH to include the globally installed packages
ENV PATH=/usr/local/bin:$PATH

# Copy application code
COPY main.py .

# Expose the port the app runs on
EXPOSE 8000

# Create a non-root user for security (Best Practice)
RUN useradd -m appuser
USER appuser

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
