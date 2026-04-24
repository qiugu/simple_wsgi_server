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