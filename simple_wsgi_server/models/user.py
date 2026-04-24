class UserModel:
    _user_db: list[dict] = []
    _id_counter = 1
    
    @classmethod
    def get_by_username(cls, username: str):
        return next((u for u in cls._user_db if u['username'] == username), None)
    
    @classmethod
    def get_by_userid(cls, userid: int):
        return next((u for u in cls._user_db if u['user_id'] == userid), None)
    
    @classmethod
    def register(cls, username: str, password: str, nickname: str):
        exist_user = cls.get_by_username(username)
        
        if exist_user:
            return None
        cls._id_counter += 1
        user = {
            'user_id': cls._id_counter,
            'username': username,
            'nickname': nickname,
            'password': password
        }
        cls._user_db.append(user)
        user_out = { k: user[k] for k in user if k != 'password' }
        return user_out
    
    @classmethod
    def login(cls, username: str, password: str):
        user = cls.get_by_username(username)
        
        if user:
            if user['password'] == password:
                return { k: v for k, v in user.items() if k != 'password' }
        return None
    
    @classmethod
    def update_user(cls, userid: int, username: str, nickname: str):
        user = cls.get_by_userid(userid)
        
        if user:
            user_copy = user.copy()
            user_copy['username'] = username
            user_copy['nickname'] = nickname
            
            return { k: user_copy[k] for k in user_copy if k != 'password' }
        return None
            
    @classmethod
    def delete_user(cls, userid: int):
        user = cls.get_by_userid(userid)
        
        if user:
            cls._user_db.remove(user)
            return True
        return False
    
    @classmethod
    def list_users(cls, limit: int, offset: int):
        total = len(cls._user_db)
        return {
            'list': cls._user_db[offset:offset+limit],
            'total': total
        }