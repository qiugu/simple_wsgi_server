from ..models.user import UserModel
from ..core.validator import ParameterValidate
from ..utils.password import hash_password, verify_password
from ..utils.token import create_user_tokens

class UserService:
    @staticmethod
    def login(username: str, password: str):
        login_user = UserModel.get_by_username(username)
        
        if login_user:
            if verify_password(password, login_user['password']):
                access_token, refresh_token = create_user_tokens(login_user)
                out_login_user = { k: v for k, v in login_user.items() if k != 'password' }
                return out_login_user, access_token, refresh_token
            else:
                return None
        else:
            return None
        
    @staticmethod
    def register(username: str, password: str, role: str):
        # 校验规则（企业级标准）
        rules = {
            "username": {"required": True, "type": str, "min_len": 3, "max_len": 20},
            "password": {"required": True, "type": str, "min_len": 6, "max_len": 20},
            "nickname": {"required": False, "type": str, "min_len": 2, "max_len": 20}
        }
        ParameterValidate.validate(locals(), rules)
        
        hash_pass = hash_password(password)
        register_user = UserModel.register(username, hash_pass, role)
        
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
    def update_user(userid: int, username: str, role: str):
        new_user = UserModel.update_user(userid, username, role)
        
        if not new_user:
            return None
        return new_user
    
    @staticmethod
    def del_user(userid: int):
        return UserModel.delete_user(userid)