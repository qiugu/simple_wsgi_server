from ..core.response import make_response
from ..models.user import UserModel
from ..core.validator import ParameterValidate

class UserService:
    @staticmethod
    def login(username: str, password: str):
        if not username or not password:
            return make_response(400, "用户名或密码不能为空", None)
        
        login_user = UserModel.login(username, password)
        
        if login_user:
            return make_response(200, '登录成功', login_user)
        else:
            return make_response(400, '账号或密码错误', None)
        
    @staticmethod
    def register(username: str, password: str, repeat_password: str, nickname: str):
        if not username or not password:
            return make_response(400, "用户名或密码不能为空", None)
        
        if password != repeat_password:
            return make_response(400, "两次输入的密码不一致", None)
        
        # 校验规则（企业级标准）
        rules = {
            "username": {"required": True, "type": str, "min_len": 3, "max_len": 20},
            "password": {"required": True, "type": str, "min_len": 6, "max_len": 20},
            "repeat_password": {"required": True, "type": str, "min_len": 6, "max_len": 20},
            "nickname": {"required": False, "type": str, "min_len": 2, "max_len": 20}
        }
        ParameterValidate.validate(locals(), rules)
        
        register_user = UserModel.register(username, password, nickname)
        
        if register_user:
            return make_response(200, "注册成功", register_user)
        return make_response(400, "用户名已存在", None)
    
    @staticmethod
    def get_user_detail(userid: int | None):
        if not userid:
            return make_response(400, "用户id不能为空", None)
        user = UserModel.get_by_userid(userid)
        if user:
            return make_response(200, "获取用户详情成功", user)
        return make_response(400, "获取用户详情失败", None)
    
    @staticmethod
    def get_all_user():
        pass
    
    @staticmethod
    def update_user(username: str, nickname: str):
        pass
    
    @staticmethod
    def del_user(userid: str):
        pass