import json

class User:

    def __init__(self, id, username, points):
        self.id = id
        self.username = username
        self.points = points

    def add_points(self, new_points):
        self.points += new_points

    def to_dict(self):
        return {
            "username": self.username,
            "points": self.points
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data):
        return User(None, data["username"], data["points"])

    @staticmethod
    def from_json(string):
        data = json.loads(string)
        return User(
            id=None,
            username=data["username"],
            points=float(data["points"]))