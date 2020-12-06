class WichtelRoom:
    def __init__(self, code):
        self.code = code
        self.members = []

    def to_dict(self):
        return {
            'code': self.code,
            'member': self.members
        }
