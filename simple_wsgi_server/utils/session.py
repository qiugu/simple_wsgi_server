import secrets

from datetime import datetime, timedelta
from ..env import SESSION_EXPIRE_HOURS

sessions = {}

def create_session(user: dict):
    session_id = secrets.token_hex(32)
    expire_time = datetime.now() + timedelta(SESSION_EXPIRE_HOURS)
    
    global sessions
    sessions[session_id] = {
        'user': user,
        'expire': expire_time
    }
    
    return session_id
    
def get_session(session_id: str):
    global sessions
    session = sessions.get(session_id)
    
    if not session:
        return None
    if datetime.now() > session['expire']:
        del sessions[session_id]
        return None
    return session

def del_session(session_id: str):
    global sessions
    
    if session_id in sessions:
        del sessions[session_id]