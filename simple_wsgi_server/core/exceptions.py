class BusinessException(Exception):
    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg
        super().__init__(msg)
        
class ParamsException(BusinessException):
    def __init__(self, msg: str = '参数错误') -> None:
        super().__init__(400, msg)