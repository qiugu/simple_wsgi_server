LOG_PATH = 'app.log'

CORS_CONFIGS = {
    'allow_origins': 'http://127.0.0.1:5500',
    "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
    'allow_headers': 'Content-Type,Authorization',
    'allow_credentials': 'true',
    'max_age': '86400'
}

SESSION_EXPIRE_HOURS = 24
SESSION_KEY = 'session_id'

PUBLIC_URLS = [
    '/api/login',
    '/api/register'
]

# jwt配置
JWT_SECRET_KEY = 'please-set-your-secrets'
JWT_ALGORITHM = 'HS256'
JWT_ACCESS_EXPIRE = 30 # 令牌访问有效期为30分钟
JWT_REFERSH_EXPIRE = 7 * 24 # 刷新令牌有效期为7天

# cookie的key设置
ACCESS_COOKIE = 'access_token'
REFRESH_COOKIE = 'refresh_token'