from models.telegram_user import TelegramUser


class WichtelRoom:
    def __init__(self, code, admin_user: TelegramUser, telegram_users):
        self.code = code
        self.admin_user = admin_user
        self.telegram_users = []

    @staticmethod
    def from_dict(dict):
        return WichtelRoom(
            code=dict.get('code'),
            admin_user=TelegramUser.from_dict(dict.get('admin_user')),
            telegram_users=[TelegramUser.from_dict(d) for d in dict.get('telegram_users')]
        )

    def to_dict(self):
        return {
            'admin_user': self.admin_user.to_dict(),
            'code': self.code,
            'telegram_users': [tu.to_dict() for tu in self.telegram_users]
        }
