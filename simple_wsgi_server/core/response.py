import json

def make_response(status_code, msg, data):
    """封装统一响应"""
    resp_message = {
        "code": status_code,
        "msg": msg,
        "data": data
    }
    
    return json.dumps(resp_message, ensure_ascii=False).encode('utf-8')