class TelegramUser:
    def __init__(self, id, first_name, username):
        self.id = id
        self.first_name = first_name
        self.username = username

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "username": self.username,
        }
