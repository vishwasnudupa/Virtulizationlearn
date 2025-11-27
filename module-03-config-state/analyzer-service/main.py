import os
import json
import time
import redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Analyzer")

# Environment Variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "logs_queue")
ALERT_KEYWORDS = os.getenv("ALERT_KEYWORDS", "ERROR,CRITICAL").split(",")

def process_log(log_data):
    """
    Simulate complex analysis logic.
    """
    message = log_data.get("message", "")
    level = log_data.get("level", "INFO")
    
    # Check for alert conditions
    if level in ALERT_KEYWORDS:
        logger.warning(f"ALERT TRIGGERED: {log_data['service_name']} reported {level}: {message}")
        # In a real app, we would send an email/Slack notification here
    else:
        logger.info(f"Processed normal log: {message}")

def main():
    logger.info("Starting Log Analyzer Service...")
    logger.info(f"Watching for keywords: {ALERT_KEYWORDS}")
    
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
        logger.info("Connected to Redis")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return

    while True:
        try:
            # BLPOP blocks until an item is available
            # It returns a tuple (queue_name, data)
            _, data = r.blpop(REDIS_QUEUE)
            log_entry = json.loads(data)
            process_log(log_entry)
        except Exception as e:
            logger.error(f"Error processing log: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
