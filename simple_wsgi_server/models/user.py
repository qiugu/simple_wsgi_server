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
    
    def update_user(self, userid: int, username: str, nickname: str):
        user = self.get_by_userid(userid)
        
        if user:
            user_copy = user.copy()
            user_copy['username'] = username
            user_copy['nickname'] = nickname
            
            return { k: v for k, v in user_copy if k != 'password' }
        return None
            
    
    def delete_user(self, userid: int):
        user = self.get_by_userid(userid)
        
        if user:
            self._user_db.remove(user)
        return None
    
    def list_users(self, limit: int, offset: int):
        total = len(self._user_db)
        return {
            'list': self._user_db[offset:offset+limit],
            'total': total
        }