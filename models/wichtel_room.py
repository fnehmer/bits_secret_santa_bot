from models.telegram_user import TelegramUser


class WichtelRoom:
    def __init__(self, code, admin_user: TelegramUser):
        self.code = code
        self.admin_user = admin_user
        self.telegram_users = []

    def from_dict(self, dict):
        return WichtelRoom(
            code=dict.get('code'),
            admin_user=dict.get('admin_user')
        )

    def to_dict(self):
        return {
            'admin_user': self.admin_user.to_dict(),
            'code': self.code,
            'telegram_users': self.telegram_users
        }
