import time
import json

from .exceptions import BusinessException, UnauthorizedException
from .request import Request
from .log import logger
from .response import make_response
from ..env import CORS_CONFIGS, PUBLIC_URLS, ACCESS_COOKIE, REFRESH_COOKIE, JWT_ACCESS_EXPIRE, JWT_REFERSH_EXPIRE
from ..utils.token import verify_token

def auth_middleware(func):
    def wrapper(environ, start_response):
        req = Request(environ)
        # 预见请求或者公共路由跳过鉴权
        if req.path in PUBLIC_URLS or req.method == 'OPTIONS':
            environ['request_obj'] = req
            return func(environ, start_response)
        token = req.get_token()
        
        if not token:
            raise UnauthorizedException()
        payload = verify_token(token)
        if not payload:
            raise UnauthorizedException()
        
        req.user = payload
        environ['request_obj'] = req
        
        return func(environ, start_response)
    return wrapper

def cors_middleware(func):
    def wrapper(environ, start_response):
        cors_res_headers = [
            ('Access-Control-Allow-Origin', CORS_CONFIGS['allow_origins']),
            ('Access-Control-Allow-Methods', CORS_CONFIGS['allow_methods']),
            ('Access-Control-Allow-Headers', CORS_CONFIGS['allow_headers']),
            ('Access-Control-Allow-Credentials', CORS_CONFIGS['allow_credentials']),
            ('Access-Control-Max-Age', CORS_CONFIGS['max_age'])
        ]
        
        # 预检请求
        method = environ.get('REQUEST_METHOD', '').upper()
        if method == 'OPTIONS':
            logger.info(f"请求 => {method}")
            start_response('200 ok', cors_res_headers)
            return []
        
        # 合并原有的响应头
        def new_start_response(status, headers):
            headers.extend(cors_res_headers)
            
            tokens = environ.get('tokens')
            
            if tokens:
                (access_token, refresh_token) = tokens
                headers.extend(
                    [
                        (
                            f"Set-Cookie",
                            f"{ACCESS_COOKIE}={access_token}; HttpOnly; Path=/; Max-Age={JWT_ACCESS_EXPIRE*60}"
                        ),
                        (
                            f"Set-Cookie",
                            f"{REFRESH_COOKIE}={refresh_token}; HttpOnly; Path=/; Max-Age={JWT_REFERSH_EXPIRE*60}"
                        )
                    ]
                )
            return start_response(status, headers)
        
        return func(environ, new_start_response)
    return wrapper

def exception_middleware(func):
    def wrapper(environ, start_response) -> bytes:
        try:
            resp = func(environ, start_response)

            # return resp
        except BusinessException as be:
            resp = make_response(be.code, be.msg, None)
        except Exception as e:
            resp = make_response(500, f"服务器内部错误: {str(e)}", None)
        return resp
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