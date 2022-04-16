import json


class ApiResponse:

    STATUS_OK = 200
    STATUS_BAD_REQUEST = 400
    STATUS_INTERNAL_SERVER_ERROR = 500
    STATUS_UNAUTHORIZED = 403
    STATUS_NOT_FOUND = 404

    def __init__(self, status, data={}):
        self.status = status
        self.data = data

    def build(self):
        return {"statusCode": self.status, "body": json.dumps(self.data)}
