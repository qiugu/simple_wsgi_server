# Simple WSGI Server

## 项目简介
Simple WSGI Server 是一个极简、易扩展的 Python WSGI Web 框架，支持路由、参数校验、日志、异常处理等功能，适合学习和快速开发小型 Web 服务。

## 安装与运行
1. 克隆项目：
	```bash
	git clone https://github.com/your-repo/simple_wsgi_server.git
	cd simple_wsgi_server
	```
2. 安装依赖（推荐 Python 3.11+）：
	```bash
	poetry install
	```
3. 启动服务：
	```bash
	poetry run start-app
	```
	默认监听地址为 http://127.0.0.1:8001

## 主要功能
- 路由注册与参数提取
- 支持 GET/POST/PUT/DELETE 等 HTTP 方法
- 统一响应格式
- 全链路日志与异常处理
- 参数校验
- 简单的用户注册、登录、信息管理接口
- 文件上传接口

## 快速上手
示例：
```python
from simple_wsgi_server.core.app import WsgiApp

app = WsgiApp()

@app.add_router('GET', '/', lambda req: ...)
def index_handler(request):
	 ...

if __name__ == '__main__':
	 app()
```

## API 列表
| 方法 | 路径                | 说明         |
|------|---------------------|--------------|
| GET  | /                   | 首页         |
| POST | /api/register       | 用户注册     |
| POST | /api/login          | 用户登录     |
| GET  | /api/users          | 用户列表     |
| GET  | /api/users/{id}     | 用户详情     |
| PUT  | /api/users/{id}     | 更新用户信息 |
| DELETE | /api/users/{id}   | 删除用户     |
| POST | /api/upload         | 文件上传     |

## 目录结构
```
simple_wsgi_server/
├── core/        # 框架核心模块（路由、请求、响应、中间件等）
├── curds/       # 业务逻辑层（如用户服务）
├── models/      # 数据模型（如用户模型）
├── views/       # 视图与接口实现
├── main.py      # 应用入口
├── __init__.py
tests/           # 测试用例
pyproject.toml   # 项目配置
README.md        # 项目说明
```

## 贡献
欢迎提交 Issue 或 PR，完善功能或修复问题。

## License
MIT
