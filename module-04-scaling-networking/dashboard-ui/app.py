from flask import Flask, render_template_string
import redis
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "logs_queue")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sentinel Dashboard</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; background-color: #f0f2f5; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: inline-block; }
        h1 { color: #1a73e8; }
        .stat { font-size: 4em; font-weight: bold; color: #333; }
        .label { color: #666; }
    </style>
    <meta http-equiv="refresh" content="2">
</head>
<body>
    <div class="card">
        <h1>Sentinel System Status</h1>
        <div class="stat">{{ queue_length }}</div>
        <div class="label">Logs in Queue</div>
        <p>Connected to Redis at: {{ redis_host }}</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        queue_len = r.llen(REDIS_QUEUE)
        return render_template_string(HTML_TEMPLATE, queue_length=queue_len, redis_host=REDIS_HOST)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, queue_length="Error", redis_host=str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
