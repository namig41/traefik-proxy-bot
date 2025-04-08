import uuid
from typing import Optional

from pyxui import XUI
from pyxui.errors import BadLogin, NotFound

from infrastracture.logger import logger
from settings import config


class XUIClient:
    def __init__(self) -> None:
        self.client: XUI = XUI(
            full_address="http://localhost:2053",
            panel="sanaei",
            https=False,
        )
        if not self.login():
            logger.critical("XUI login unsuccessful")

        self.default_inbound_id: int = 1

    def get_server_info(self) -> dict:
        return self.client.get_inbound(self.default_inbound_id)["obj"]

    def get_client(self, client_id: str) -> Optional[dict]:
        res = self.client.get_client(self.default_inbound_id, client_id)

        if res is NotFound:
            return None

        return res

    def create_client(self, prefix: str) -> str:
        client_uuid = str(uuid.uuid4())

        client_id = prefix + "_" + client_uuid if prefix else client_uuid

        self.client.add_client(
            self.default_inbound_id,
            client_id,
            client_uuid,
        )

        return client_uuid

    def delete_client(self, client_id: str) -> bool:
        try:
            self.client.delete_client(
                self.default_inbound_id,
                client_id,
            )
        except Exception:
            return False

        return True

    def login(self) -> bool:
        try:
            self.client.login(
                username=config.XUI_USERNAME,
                password=config.XUI_PASSWORD,
            )
        except BadLogin:
            return False

        return True


xui_engine = XUIClient()
