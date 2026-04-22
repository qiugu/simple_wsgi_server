import time
import json

from .exceptions import BusinessException
from .request import Request
from .log import logger
from .response import make_response

def exception_middleware(func):
    def wrapper(environ, start_response):
        try:
            res = func(environ, start_response)
            
            return res
        except BusinessException as be:
            resp = make_response(be.code, be.msg, None)
        except Exception as e:
            resp = make_response(500, f"服务器内部错误: {str(e)}", None)
        
        status = '200 OK'
        headers = [('Content-Type', 'application/json;charset=utf-8')]
        start_response(status, headers)
        return [resp]
    return wrapper

def log_middleware(func):
    def wrapper(environ, start_response):
        start_time = time.time()
        req = Request(environ)
        
        logger.info(f"请求 => {req.method} {req.path} | 查询参数: {req.query_params} | 请求体: {req.form_data}")
        
        try:
            res = func(environ, start_response)
            cost = round(time.time() - start_time, 2)
            resp_data = json.loads(res[0].decode('utf-8'))
            logger.info(f"响应 => {req.method} {req.path} | 耗时：{cost}s | 响应体：{resp_data}")
            
            return res
        except Exception as e:
            cost = round(time.time() - start_time, 2)
            logger.error(f"异常 => {req.method} {req.path} | 耗时：{cost} | 错误：{str(e)}", exc_info=True)
            raise
    return wrapper