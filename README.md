# 2024BUAA_DB_Homework
## 项目简介

北航猫猫管理平台是一个基于 Web 的平台，我们希望通过这样一个校园猫猫管理平台，连接起所有爱心，为这些猫猫提供一个更有保障的生活环境。

## 技术栈

- **前端**：
  - 使用 **Vue 3** 来构建现代化、响应式的用户界面。
  - **Vue Router** 用于前端路由管理，**Vuex** 用于状态管理。
  - 地图展示通过高德地图API实现。
  
- **后端**：
  - 使用 **FastAPI** 作为 Web 框架，提供 RESTful API 接口。
  - **MySQL** 数据库存储用户、猫咪、以及猫咪位置的数据。
  - **SQLModel**（基于 SQLAlchemy）用于数据库建模，支持自动迁移。
  - **JWT** 用户鉴权机制，通过生成 Access Token 实现安全验证。

## 后端

### 技术说明

1. **FastAPI** 提供了一个高性能的后端框架，所有的 API 都采用 **RESTful** 风格。
2. 用户可以通过 **JWT** Token 登录后进行身份验证，并访问受保护的路由。
3. **JWT** Token 用于用户身份验证，登录后会返回一个 `access_token`，前端每次请求时需要将其作为 Authorization 头发送。

### 数据库配置说明

项目使用MySQL数据库。在启动程序之前，请先开启MySQL Server，检查Schema是否正确添加。（项目建议统一新建一个额外的Schema: `CatsTrack`，当然你也可以使用任意已有的Schema。）

确保在启动应用之前，项目目录(`backend/app/`)下已经有`mysql_config.py`文件，并添加如下变量到文件中：
```python
mysql_user = "your_username"
mysql_password = "your_password"
mysql_host = "localhost:port_number"
mysql_db_schema = "your_db_schema_name"
``` 

### 运行后端

1. 安装依赖：

```bash
  pipenv install
```

2. 启动应用：

```bash
  fastapi dev
```
您可以在[http://localhost:8000/docs/](http://localhost:8000/docs)访问fastapi生成的API文档页面。

## 前端

### 技术说明

1. **Vue 3** 用于构建前端，提供响应式界面，使用 **Vue Router** 管理路由。
2. 用户可以通过地图界面查看猫咪的实时位置，上传新位置。
3. 用户需要通过前端界面登录，登录后将会接收一个 `JWT` token，用于后续的 API 请求。

### 运行前端

1. 安装依赖：

```bash
  pnpm install
```

2. 启动开发服务器：

```bash
  pnpm dev
```
您可以在[http://localhost:3000/](http://localhost:3000/)访问前端页面。