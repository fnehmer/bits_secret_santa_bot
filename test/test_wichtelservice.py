import json
import unittest

from models.telegram_user import TelegramUser
from models.wichtel_room import WichtelRoom
from wichtel_service import WichtelService


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.tu_1 = TelegramUser(id='123', first_name="Enton Relaxo", username='relax')
        self.tu_2 = TelegramUser(id='456', first_name="Ash Misty", username='pickachu')
        self.tu_3 = TelegramUser(id='789', first_name="Barney Stinson", username='himym')
        self.wr_1 = WichtelRoom(code='lasj123', admin_user=self.tu_3)

    def test_save_state(self):
        ws = WichtelService()
        ws.telegram_users = [self.tu_1, self.tu_2]
        ws.wichtel_rooms = [self.wr_1]
        ws.save_state(data_dir='test/data')

        expected_users = [
            {"first_name": "Enton Relaxo", "id": "123", "username": "relax"},
            {"first_name": "Ash Misty", "id": "456", "username": "pickachu"}]
        expected_rooms = [
            {
                "admin_user": {"first_name": "Barney Stinson", "id": "789", "username": "himym"},
                "code": "lasj123",
                "telegram_users": []
            }
        ]
        with open('test/data/telegram_users.json') as file:
            self.assertListEqual(expected_users, json.load(file))

        with open('test/data/wichtel_rooms.json') as file:
            self.assertListEqual(expected_rooms, json.load(file))

    def test_load_state(self):
        ws = WichtelService()
        ws.load_state(data_dir='test/data')

        expected_users = [
            {"first_name": "Enton Relaxo", "id": "123", "username": "relax"},
            {"first_name": "Ash Misty", "id": "456", "username": "pickachu"}]
        expected_rooms = [
            {
                "admin_user": {"first_name": "Barney Stinson", "id": "789", "username": "himym"},
                "code": "lasj123",
                "telegram_users": []
            }
        ]
        self.assertListEqual(expected_users, ws.telegram_users)
        self.assertListEqual(expected_rooms, ws.wichtel_rooms)
