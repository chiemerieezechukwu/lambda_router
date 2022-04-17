import json


class Response:
    def __init__(self, status, data=None):
        self.status = status
        self.data = data

    def build(self):
        return {"statusCode": self.status, "body": json.dumps(self.data)}
