from ..core.request import Request
from ..curds.user import UserService

class UserView:
    @staticmethod
    def login(request: Request):
        username = request.form_data.get('username', '')
        password = request.form_data.get('password', '')
        
        return UserService.login(username, password)
    
    @staticmethod
    def register(request: Request):
        username = request.form_data.get('username', '')
        password = request.form_data.get('password', '')
        nickname = request.form_data.get('nickname', '')
        repeat_password = request.form_data.get('repeat_password', '')
        
        return UserService.register(username, password, repeat_password, nickname)
    
    @staticmethod
    def update(request: Request):
        username = request.form_data.get('username', '')
        nickname = request.form_data.get('nickname', '')
        
        return UserService.update_user(username, nickname)
    
    @staticmethod
    def delete(request: Request):
        userid = request.path_params.get('id')
        
        if userid:
            UserService.del_user(userid)
        return False
    
    @staticmethod
    def user_detail(request: Request):
        userid_str = request.path_params.get('id', '')
        
        if userid_str != '':
            userid = int(userid_str)
        else:
            userid = None
        
        return UserService.get_user_detail(userid)
    
    @staticmethod
    def all_users(request: Request):
        pass