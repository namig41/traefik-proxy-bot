from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str

    XUI_URL: str
    XUI_USERNAME: str
    XUI_PASSWORD: str
    XUI_HOSTNAME: str
    XUI_PANEL_PORT: int
    XUI_EMAIL: str

    TELEGRAM_API_TOKEN: str
    TELEGRAM_ADMIN_ID: str

    SQLITE_DB_PATH: str

    LOG_PATH_DIR: str


config = Settings()
