import json


class ApiRequest:
    def __init__(self, event: dict, context=None):
        self.event = event
        self.context = context

    def query_params(self):
        _ret = {}
        for key, value in self.event.get("queryStringParameters", {}).items():
            if len(value.split(",")) == 1:
                _ret[key] = value.split(",")[0]
            else:
                _ret[key] = value.split(",")
        return _ret

    def request_context(self):
        return self.event["requestContext"]

    def http(self):
        return self.request_context().get("http")

    @property
    def path(self):
        return self.http().get("path")

    @property
    def body(self):
        return json.loads(self.event.get("body", "{}"))

    @property
    def method(self):
        return self.http().get("method", "GET").upper()

    @property
    def args(self):
        return self.query_params()

    def get_method(self):
        return self.event["httpMethod"]
