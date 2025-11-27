import os
import json
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import redis
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentinel Log Collector")

# Environment Variables (Best Practice: Configuration via Env Vars)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "logs_queue")

# Initialize Redis Connection
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()
    logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    # In a real app, we might want to exit or retry, but for this demo we'll continue
    # and fail on requests if Redis is down.

class LogEntry(BaseModel):
    service_name: str
    level: str
    message: str
    timestamp: str = None

@app.post("/logs")
async def collect_log(entry: LogEntry):
    """
    Endpoint to receive logs from various services.
    Pushes the log entry to a Redis list (queue) for asynchronous processing.
    """
    if not entry.timestamp:
        entry.timestamp = datetime.utcnow().isoformat()

    log_data = entry.model_dump()
    
    try:
        # LPUSH adds the element to the head of the list
        redis_client.lpush(REDIS_QUEUE, json.dumps(log_data))
        logger.info(f"Received log from {entry.service_name}: {entry.message}")
        return {"status": "queued", "queue_length": redis_client.llen(REDIS_QUEUE)}
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        raise HTTPException(status_code=503, detail="Log storage temporarily unavailable")

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint for container orchestrators (K8s probes).
    """
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
