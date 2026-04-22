from ..core.request import Request
from ..core.response import make_response

import os

def index_handler(request: Request):
    """首页"""
    return make_response(200, '欢迎访问极简WSGI服务', request.query_params)

def upload_file(request: Request):
    """上传文件"""
    result = {}
    for name, field in request.files:
        save_path = f"./{field.filename}"
        result[name] = {
            "filename": field.filename,
            "save_path": save_path,
            "file_size": os.path.getsize(save_path)
        }
    return make_response(200, '文件上传成功', {
        "form_data": request.form_data,
        "files": result
    })