from .exceptions import Exception404, Exception405
from .helpers import ApiRequest


class LambdaRouter:
    def __init__(self):
        self._routes = {}
        self._request_class = None

    def route(self, path, methods=["GET"]):
        """Register a route to it's corresponding function"""

        def decorator(func):
            if path in self._routes:
                raise ValueError(f"Duplicate route: '{path}'")
            self._routes[path] = {"function": func, "allowed_methods": [method.upper() for method in methods]}
            return func

        return decorator

    def set_request_class(self, request_class):
        """You can set the request class instead of using the default `ApiRequest`"""
        self._request_class = request_class

    def get_request_class(self):
        """Get the request class"""
        return self._request_class or ApiRequest

    def handle_options(self, request):
        """Handle OPTIONS requests"""
        return ", ".join(self.list_routes()[request.path])

    def run(self, event, context=None, *args, **kwargs):
        """Run the requested route"""
        request = self.get_request_class()(event, context)

        if request.path not in self._routes:
            raise Exception404(f"Route not found: '{request.path}'")

        if request.method not in self._routes[request.path]["allowed_methods"]:
            raise Exception405(f"Method not allowed: '{request.method}'")

        if request.method == "OPTIONS":
            return f"{self.handle_options(request)}"

        return self._routes[request.path]["function"](request, *args, **kwargs)

    def list_routes(self):
        """List all registered routes"""
        return {k: v["allowed_methods"] for k, v in self._routes.items()}
