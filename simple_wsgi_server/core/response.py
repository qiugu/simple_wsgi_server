import json

def make_response(status_code, msg, data = None):
    """封装统一响应"""
    resp_message = {
        "code": status_code,
        "msg": msg,
        "data": data
    }
    
    return json.dumps(resp_message, ensure_ascii=False).encode('utf-8')

def decode_data(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    if isinstance(data, dict):
        return { k: decode_data(v) for k, v in data.items() }
    if isinstance(data, list):
        return [decode_data(item) for item in data]
    return data