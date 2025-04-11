import logging
import os
from datetime import datetime

from settings import config


logger = logging.getLogger()

os.makedirs(config.LOG_PATH_DIR, exist_ok=True)

# Создаем обработчик для записи в файл
current_date = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(config.LOG_PATH_DIR, f"unit_api_{current_date}.log")

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

# Создаем обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Формат логов
formatter = logging.Formatter(
    fmt="%(levelname)-8s %(asctime)s | %(module)-10s:%(lineno)-10d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)
