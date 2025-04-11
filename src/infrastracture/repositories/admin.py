from settings import config


class AdminRepository:
    def __init__(self):
        self.admin = config.TELEGRAM_ADMIN_ID
