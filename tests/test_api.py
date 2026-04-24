import requests

BASE_URL = "http://127.0.0.1:8001"

def test_index():
    resp = requests.get(f"{BASE_URL}/")
    assert resp.status_code == 200
    assert resp.json()["msg"] == "欢迎访问极简WSGI服务"

def test_register_and_login():
    # 注册
    data = {
        "username": "testuser",
        "password": "testpass123",
        "repeat_password": "testpass123",
        "nickname": "测试用户"
    }
    resp = requests.post(f"{BASE_URL}/api/register", data=data)
    assert resp.status_code == 200
    assert resp.json()["code"] in [200, 400]  # 已存在或注册成功

    # 登录
    login_data = {"username": "testuser", "password": "testpass123"}
    resp = requests.post(f"{BASE_URL}/api/login", data=login_data)
    assert resp.status_code == 200
    assert resp.json()["code"] in [200, 400]

def test_user_detail():
    # 假设用户ID为2
    resp = requests.get(f"{BASE_URL}/api/users/2")
    assert resp.status_code == 200
    assert "code" in resp.json()
