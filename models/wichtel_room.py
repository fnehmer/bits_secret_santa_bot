class WichtelRoom:
    def __init__(self, code):
        self.code = code
        self.members = []

    def from_dict(self, dict):
        return WichtelRoom(
            code=dict.get('code'),
        )

    def to_dict(self):
        return {
            'code': self.code,
            'member': self.members
        }
