from .core.app import WsgiApp
from .views.index import index_handler, upload_file
from .views.user import UserView

app = WsgiApp()

app.add_router('GET', '/', index_handler)
app.add_router('POST', '/api/register', UserView.register)
app.add_router('POST', '/api/login', UserView.login)

app.add_router('GET', '/api/users', UserView.all_users)
app.add_router('GET', '/api/users/{id}', UserView.user_detail)
app.add_router('PUT', '/api/users/{id}', UserView.update)
app.add_router('DELETE', '/api/users/{id}', UserView.delete)

app.add_router('POST', '/api/upload', upload_file)