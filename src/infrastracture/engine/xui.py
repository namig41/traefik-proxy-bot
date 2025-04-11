import uuid
from typing import Optional

from infrastracture.logger import logger
from pyxui import XUI
from pyxui.errors import (
    BadLogin,
    NotFound,
)
from settings import config


class XUIClient:
    def __init__(self) -> None:
        self.client: XUI = XUI(
            full_address="http://localhost:2053",
            panel="sanaei",
            https=False,
        )

        self.default_inbound_id: int = 1
        if not self.login():
            logger.critical("❌ XUI login unsuccessful")

    def get_server_info(self) -> dict:
        """Получить информацию о сервере."""
        try:
            return self.client.get_inbound(self.default_inbound_id)["obj"]
        except Exception as e:
            logger.error(f"Ошибка при получении информации о сервере: {e}")
            return {}

    def get_client(self, client_id: str) -> Optional[dict]:
        """Получить клиента по ID."""
        try:
            res = self.client.get_client(self.default_inbound_id, client_id)
            return None if res is NotFound else res
        except Exception as e:
            logger.error(f"Ошибка при получении клиента '{client_id}': {e}")
            return None

    def create_client(self, prefix: str = "") -> str:
        """Создать нового клиента с UUID и префиксом."""
        client_uuid = str(uuid.uuid4())
        client_id = f"{prefix}_{client_uuid}" if prefix else client_uuid

        try:
            self.client.add_client(self.default_inbound_id, client_id, client_uuid)
            logger.info(f"✅ Клиент создан: {client_id}")
        except Exception as e:
            logger.error(f"Ошибка при создании клиента '{client_id}': {e}")
            raise

        return client_uuid

    def delete_client(self, client_id: str) -> bool:
        """Удалить клиента по ID."""
        try:
            self.client.delete_client(self.default_inbound_id, client_id)
            logger.info(f"🗑 Клиент удалён: {client_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при удалении клиента '{client_id}': {e}")
            return False

    def login(self) -> bool:
        """Войти в панель XUI."""
        try:
            self.client.login(
                username=config.XUI_USERNAME,
                password=config.XUI_PASSWORD,
            )
            logger.info("🔐 Успешный вход в XUI")
            return True
        except BadLogin:
            logger.warning("❗ Неверные учётные данные XUI")
            return False
        except Exception as e:
            logger.error(f"Ошибка при попытке входа в XUI: {e}")
            return False


xui_engine = XUIClient()
