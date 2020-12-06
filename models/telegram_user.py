from telegram import User


class TelegramUser:
    def __init__(self, id, first_name, username):
        self.id = id
        self.first_name = first_name
        self.username = username

    @staticmethod
    def from_telegram_user_object(telegram_user_object: User):
        return TelegramUser(
            id=telegram_user_object.id,
            first_name=telegram_user_object.first_name,
            username=telegram_user_object.username
        )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "username": self.username,
        }
