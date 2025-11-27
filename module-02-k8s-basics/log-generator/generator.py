import time
import random
import requests
import os
import logging

# Configuration
COLLECTOR_URL = os.getenv("COLLECTOR_URL", "http://localhost:8000/logs")
INTERVAL = float(os.getenv("INTERVAL", "1.0"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("LogGenerator")

SERVICES = ["payment-service", "auth-service", "inventory-service", "notification-service"]
LEVELS = ["INFO", "INFO", "INFO", "WARNING", "ERROR"]
MESSAGES = {
    "payment-service": ["Transaction processed", "Payment declined", "Gateway timeout"],
    "auth-service": ["User login", "Token refreshed", "Invalid credentials"],
    "inventory-service": ["Stock updated", "Item not found", "Warehouse sync"],
    "notification-service": ["Email sent", "SMS delivered", "Template error"]
}

def generate_log():
    service = random.choice(SERVICES)
    level = random.choice(LEVELS)
    message = random.choice(MESSAGES[service])
    
    return {
        "service_name": service,
        "level": level,
        "message": message
    }

def main():
    logger.info(f"Starting Log Generator. Target: {COLLECTOR_URL}")
    while True:
        try:
            log_data = generate_log()
            response = requests.post(COLLECTOR_URL, json=log_data, timeout=2)
            if response.status_code == 200:
                logger.info(f"Sent: {log_data['service_name']} - {log_data['message']}")
            else:
                logger.warning(f"Failed to send: {response.status_code}")
        except Exception as e:
            logger.error(f"Connection error: {e}")
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
