from infrastracture.repositories.admin import AdminRepository as AdminRepo


class Admin:
    def __init__(self):
        self.admin_repo = AdminRepo()

    def is_admin(self, telegram_id: str) -> bool:
        return self.admin_repo.admin.id == telegram_id
