import json
import os


class WichtelService:
    def __init__(self):
        self.telegram_users = []
        self.wichtel_rooms = []

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
            self.telegram_users = json.load(file)

        with open(data_dir + '/wichtel_rooms.json', "r") as file:
            self.wichtel_rooms = json.load(file)


if __name__ == '__main__':
    wichtel_service = WichtelService()
    # wichtel_service.telegram_users = [tu_1, tu_2]
    # wichtel_service.wichtel_rooms = [wr_1]
    # wichtel_service.save_state()

    wichtel_service.load_state()
    print(wichtel_service.telegram_users)
    print(wichtel_service.wichtel_rooms)
