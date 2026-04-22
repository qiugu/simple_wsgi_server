import re

from .request import Request
from .response import make_response

class Router:
    def __init__(self) -> None:
        self.router = []
        
    @staticmethod
    def __404_router(request: Request):
        return make_response(404, '接口不存在', None)
        
    def add_router(self, method, path, handler):
        pattern = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', path)
        regexp = re.compile(f"^{pattern}$")
        self.router.append((method.upper(), regexp, handler, path))
        
    def handle(self, request: Request) -> bytes:
        for method, regexp, handler, _ in self.router:
            if request.method == method:
                match = regexp.match(request.path)
                
                if match:
                    request.path_params = match.groupdict()
                    return handler(request)
        return self.__404_router(request)