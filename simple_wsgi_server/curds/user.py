from ..models.user import UserModel
from ..core.validator import ParameterValidate
from ..utils.password import hash_password, verify_password
from ..utils.session import create_session

class UserService:
    @staticmethod
    def login(username: str, password: str):
        login_user = UserModel.get_by_username(username)
        
        if login_user:
            if verify_password(password, login_user['password']):
                session_id = create_session(login_user)
                out_login_user = { k: v for k, v in login_user.items() if k != 'password' }
                return out_login_user, session_id
            else:
                return None
        else:
            return None
        
    @staticmethod
    def register(username: str, password: str, repeat_password: str, nickname: str):
        # 校验规则（企业级标准）
        rules = {
            "username": {"required": True, "type": str, "min_len": 3, "max_len": 20},
            "password": {"required": True, "type": str, "min_len": 6, "max_len": 20},
            "repeat_password": {"required": True, "type": str, "min_len": 6, "max_len": 20},
            "nickname": {"required": False, "type": str, "min_len": 2, "max_len": 20}
        }
        ParameterValidate.validate(locals(), rules)
        
        hash_pass = hash_password(password)
        register_user = UserModel.register(username, hash_pass, nickname)
        
        if register_user:
            return register_user
        return None
    
    @staticmethod
    def get_user_detail(userid: int):
        user = UserModel.get_by_userid(userid)
        if user:
            out_user = { k: user[k] for k in user if k != 'password' }
            return out_user
        return None
    
    @staticmethod
    def get_all_user(limit: int, offset: int):
        users = UserModel.list_users(limit, offset)
        user_list = users['list']
        out_user_list = [{k: v for k, v in u.items() if k != 'password'} for u in user_list]
        
        return {
            'list': out_user_list,
            'total': users['total']
        }
    
    @staticmethod
    def update_user(userid: int, username: str, nickname: str):
        new_user = UserModel.update_user(userid, username, nickname)
        
        if not new_user:
            return None
        return new_user
    
    @staticmethod
    def del_user(userid: int):
        return UserModel.delete_user(userid)