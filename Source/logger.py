import logging, os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M')}.log"
LOGS_PATH = os.path.join(os.getcwd(), "LOGS", LOG_FILE)
os.makedirs(LOGS_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s]-line no-%(lineno)d-filepath-%(pathname)s- %(levelname)s-%(message)s",
    level=logging.INFO,
)