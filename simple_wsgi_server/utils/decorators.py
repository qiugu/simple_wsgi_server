from typing import List
from ..core.request import Request
from ..core.exceptions import PermissionDeniedError

def permission_required(roles: List[str]):
    def decorator(func):
        def wrapper(req: Request):
            if not req.user or req.user['role'] not in roles:
                raise PermissionDeniedError()
            return func(req)
        return wrapper
    return decorator
