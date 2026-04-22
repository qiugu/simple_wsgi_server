from typing import Any, Callable
from .router import Router
from .request import Request
from .log import logger
from .middlewares import log_middleware, exception_middleware

from wsgiref.simple_server import make_server

class WsgiApp:
    def __init__(self) -> None:
        self.router = Router()
        
    def add_router(self, method: str, path: str, handler: Callable):
        self.router.add_router(method, path, handler)
        
    def _create_app(self):
        def wsgi_app(environ, start_response):
            request = Request(environ=environ)
            logger.debug(f"异常中间件")
            # logger.debug(f"请求参数：{request.__repr__()}")
            response_body = self.router.handle(request)
            
            status = '200 OK'
            headers = [('Content-Type', 'application/json;charset=utf-8')]
            start_response(status, headers)
            
            return [response_body]
        
        return log_middleware(exception_middleware(wsgi_app))
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        app = self._create_app()
        server = make_server("127.0.0.1", 8001, app)
        logger.info("="*50)
        logger.info("✅ 服务启动成功：http://127.0.0.1:8001")
        logger.info("✅ 已启用：参数校验 + 全链路日志")
        logger.info("✅ 日志文件：app.log (按天分割)")
        logger.info("="*50)
        server.serve_forever()