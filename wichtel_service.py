import json
import os

from models.telegram_user import TelegramUser
from models.wichtel_room import WichtelRoom


class WichtelService:
    def __init__(self):
        self.telegram_users = []
        self.wichtel_rooms = []

    def add_user_to_group(self, telegram_user, code):
        for wichtel_room in self.wichtel_rooms:
            if wichtel_room.code == code:
                wichtel_room.telegram_users.append(telegram_user)
                wichtel_room.telegram_users = set(wichtel_room.telegram_users)
                self.save_state()
                return wichtel_room
        return None

    def save_state(self, data_dir='data'):
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        with open(data_dir + '/telegram_users.json', "w") as file:
            serializable = [tu.to_dict() for tu in self.telegram_users]
            json.dump(serializable, file, indent=4, sort_keys=True)

        with open(data_dir + '/wichtel_rooms.json', "w") as file:
            serializable = [wr.to_dict() for wr in self.wichtel_rooms]
            json.dump(serializable, file, indent=4, sort_keys=True)

    def load_state(self, data_dir='data'):
        if not os.path.exists(data_dir):
            return

        with open(data_dir + '/telegram_users.json', "r") as file:
            data = json.load(file)
            self.telegram_users = [TelegramUser.from_dict(d) for d in data]

        with open(data_dir + '/wichtel_rooms.json', "r") as file:
            data = json.load(file)
            self.wichtel_rooms = [WichtelRoom.from_dict(d) for d in data]
