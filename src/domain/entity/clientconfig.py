from dataclasses import dataclass


@dataclass
class ClientConfig:
    id: str
    user_id: str | None
    comment: str | None
