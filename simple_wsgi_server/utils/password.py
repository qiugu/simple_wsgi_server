import bcrypt

def hash_password(raw_password: str):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
    
    return hash.decode('utf-8')

def verify_password(raw_password: str, hash_password: str):
    return bcrypt.checkpw(
        raw_password.encode('utf-8'),
        hash_password.encode('utf-8')
    )