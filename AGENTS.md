# AGENTS.md

## 项目智能体（Agents）说明

本项目可集成或扩展多种智能体（Agent）能力，便于自动化测试、代码生成、API 调用等。

### 1. 代码测试 Agent
- 功能：自动运行项目内的测试用例，检查各模块功能是否正常。
- 使用方式：
  - 运行 `pytest` 或 `python -m unittest discover`。
  - 可集成到 CI/CD 流程。

### 2. API 测试 Agent
- 功能：自动化测试 HTTP API 接口，验证接口的正确性和健壮性。
- 推荐工具：Postman、pytest + requests、httpx。
- 示例：见下方测试用例。

### 3. 文档生成 Agent
- 功能：根据代码和注释自动生成 API 文档。
- 推荐工具：Sphinx、pdoc、mkdocs。

---

## 示例测试用例

以下为部分 API 的 pytest 测试用例示例，可放置于 `tests/` 目录下：

```python
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
```

> 更多测试可参考 API 列表自行补充。

---

## 扩展说明
- 可根据实际业务需求扩展更多 Agent 能力，如自动化部署、性能测试等。
- 建议所有 Agent 相关脚本和配置统一放置于 `agents/` 或 `tests/` 目录下。
