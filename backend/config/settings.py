import logging
import os
REDIS_URI = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
REDIS_MAX_CONNECTIONS = 100

STREAMS = os.getenv("STREAMS", "ethusdt@ticker/solusdt@ticker/btcusdt@ticker")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)