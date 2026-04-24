from ..core.request import Request
from ..curds.user import UserService
from ..core.response import make_response

class UserView:
    @staticmethod
    def login(request: Request):
        username = request.form_data.get('username', '')
        password = request.form_data.get('password', '')
        
        if not username or not password:
            return make_response(400, '用户名或密码不能为空')
        
        login_user = UserService.login(username, password)
        if login_user:
            (user, access_token, refresh_token) = login_user
            request.environ['tokens'] = (access_token, refresh_token)
            return make_response(200, '登录成功', user)
        return make_response(400, '账号或密码错误')
    
    @staticmethod
    def register(request: Request):
        username = request.form_data.get('username', '')
        password = request.form_data.get('password', '')
        role = request.form_data.get('role', '')
        repeat_password = request.form_data.get('repeat_password', '')
        
        if not username or not password:
            return make_response(400, "用户名或密码不能为空", None)
        
        if password != repeat_password:
            return make_response(400, "两次输入的密码不一致")
        
        register_user = UserService.register(username, password, role)
        if register_user:
            return make_response(200, "注册成功", register_user)
        return make_response(400, "用户名已存在")
    
    @staticmethod
    def update(request: Request):
        username = request.form_data.get('username', '')
        role = request.form_data.get('role', '')
        userid = request.path_params.get('id', '')
        
        if userid == '':
            return make_response(400, '用户id不存在')
        
        new_user = UserService.update_user(int(userid), username, role)
        if new_user:
            return make_response(200, '用户更新成功', new_user)
        return make_response(400, '用户更新失败')
    
    @staticmethod
    def delete(request: Request):
        userid = request.path_params.get('id')
        
        if userid:
            is_del = UserService.del_user(int(userid))
            if is_del:
                return make_response(200, "删除成功")
            return make_response(400, "删除失败")
        return make_response(400, "用户id不存在")
    
    @staticmethod
    def user_detail(request: Request):
        userid_str = request.path_params.get('id', '')
        
        if userid_str != '':
            userid = int(userid_str)
        else:
            return make_response(400, "用户id不能为空")
        
        user = UserService.get_user_detail(userid)
        if user:
            return make_response(200, "获取用户详情成功", user)
        return make_response(400, "获取用户详情失败")
    
    @staticmethod
    def all_users(request: Request):
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)
        
        user_list = UserService.get_all_user(limit, offset)
        return make_response(200, "获取用户列表成功", user_list)