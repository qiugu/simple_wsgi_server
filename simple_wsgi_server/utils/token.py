from datetime import datetime, timedelta
from ..env import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_EXPIRE, JWT_REFERSH_EXPIRE
import jwt

def create_token(payload: dict, expire_minites: int):
    expire_time = datetime.now() + timedelta(minutes=expire_minites)
    data = { **payload, 'exp': expire_time }
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def create_user_tokens(user: dict):
    payload = { 'user_id': user['user_id'], 'username': user['username'], 'role': user['role'] }
    access_token  = create_token(payload, JWT_ACCESS_EXPIRE)
    refresh_token = create_token(payload, JWT_REFERSH_EXPIRE)
    return access_token, refresh_token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError, Exception):
        return None