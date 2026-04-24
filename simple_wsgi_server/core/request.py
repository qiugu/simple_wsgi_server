import json
import cgi
import urllib.parse
import io

from .response import decode_data
from ..env import ACCESS_COOKIE

class Request:
    def __init__(self, environ) -> None:
        self.environ = environ
        self.path = environ.get('PATH_INFO', '/')
        self.method = environ.get('REQUEST_METHOD', 'GET').upper()
        self.query_params = {}
        self.path_params = {}
        self.form_data = {}
        self.json = {}
        self.files = {}
        self.cookies = {}
        self.user = {}
        self._parse_all_params()
        self._parse_cookies()

    def __repr__(self) -> str:
        return f"""
        path: {self.path}
        method: {self.method}
        query_params: {self.query_params}
        path_params: {self.path_params}
        form_data: {self.form_data}
        json: {self.json}
        files: {self.files}
        """
        
    def _parse_cookies(self):
        cookie_str = self.environ.get('HTTP_COOKIE', '')
        cookies = [c.split('=', 1) for c in cookie_str.split(';') if '=' in c]
        self.cookies = {k.strip(): v.strip() for k, v in cookies}
        
    def get_token(self):
        # 优先从请求头获取token
        auth_header = self.environ.get('HTTP_AUTHORIZATION', '')
        if auth_header:
            if auth_header.startswith('Bearer '):
                return auth_header.split(' ')[1]
        return self.cookies.get(ACCESS_COOKIE)
        
    def _parse_all_params(self):
        query_str = self.environ.get('QUERY_STRING', '')
        self.query_params = dict(urllib.parse.parse_qsl(query_str))
        content_length_str = self.environ.get('CONTENT_LENGTH', '0')
        content_length = int(content_length_str) if content_length_str else 0
        
        if content_length == 0:
            return
        
        content_type = self.environ.get('CONTENT_TYPE')
        wsgi_input = self.environ["wsgi.input"]
        body = wsgi_input.read(content_length)
        # wsgi.input是一个流，只能读取一次，所以需要再次将流写入wsgi.input中
        self.environ["wsgi.input"] = io.BytesIO(body)
        
        if content_type.startswith('application/json'):
            try:
                self.json = json.loads(body.decode('utf-8'))
            except Exception as e:
                self.json = {}
        elif content_type.startswith('application/x-www-form-urlencoded'):
            try:
                self.form_data = dict(urllib.parse.parse_qsl(body.decode('utf-8')))
            except Exception as e:
                self.form_data = {}
        elif content_type.startswith('multipart/form-data'):
            try:
                form = cgi.FieldStorage(fp=self.environ['wsgi.input'], environ=self.environ, keep_blank_values=True)
                
                for key in form.keys():
                    field = form[key]
                    if field.filename:
                        self.files[key] = field
                    else:
                        self.form_data[key] = field.value
            except:
                pass