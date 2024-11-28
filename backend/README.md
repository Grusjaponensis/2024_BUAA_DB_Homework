# 后端程序运行说明

## 环境准备

确保你的开发环境中已经安装了 Python 3.10 或更高版本。可以通过以下命令检查 Python 版本：

```bash
python --version
# 或者
python3 --version
```

## 数据库配置说明

项目使用MySQL数据库。在启动程序之前，请先开启MySQL Server，检查Schema是否正确添加。（项目建议统一新建一个额外的Schema: `CatsTrack`，当然你也可以使用任意已有的Schema。）

确保在启动应用之前，项目目录(`app/`)下已经有`mysql_config.py`文件，并添加如下变量到文件中：
```python
mysql_user = "your_username"
mysql_password = "your_password"
mysql_host = "localhost:port_number"
mysql_db_schema = "your_db_schema_name"
``` 

## 使用 Pipenv 安装依赖

1. **安装 Pipenv**

   如果你还没有安装 Pipenv，可以通过以下命令安装：

   ```bash
   pip install pipenv
   ```

2. **安装依赖**

   在项目根目录下运行以下命令来安装依赖：

   ```bash
   pipenv install
   ```

## 数据库迁移相关
每次进行`git pull`操作后，都可能涉及到数据库表结构的变更，需要进行数据库迁移。

使用如下的命令来迁移数据库到最新版本：

```bash
alembic upgrade head
```

## 初始化数据库
通过运行根目录下的`init.sql`文件来初始化数据库。你可以选择在任一种可以与MySQL数据库交互的工具中执行这些命令。


## 启动 FastAPI
在启动 FastAPI 之前，请确保你已经完成了以上的环境准备和数据库配置、迁移步骤。请注意，**每一次 `git pull` 操作后，都需要重新运行上述数据库迁移步骤！**

1. **激活虚拟环境**

   运行以下命令激活 Pipenv 虚拟环境：

   ```bash
   pipenv shell
   ```

2. **启动 FastAPI 应用**

   在项目根目录下，运行以下命令启动 FastAPI 应用：

   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. **访问 API**

   启动后，通过访问以下 URL 来查看 API 文档：

   ```
   http://127.0.0.1:8000/docs
   ```

   可以在此页面测试和查看所有可用的 API 接口。

4. **停止 FastAPI 应用**

   按 `Ctrl+C` 停止 FastAPI 应用。



如有任何问题，请随时联系我。
