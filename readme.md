# Quqi-Admin-Flask

QuqiAdminFlask是根据LayuiAdmin + Flask开发的后台管理系统

# 项目目录

```text
quqi-admin-flask
├─logs # 日志文件
├─quqi # app包
│ ├─apis # 项目api
│ ├─common # 项目的封装的一些工具
│ ├─extensions # 项目的插件
│ ├─models # 项目的ORM模型文件
│ ├─views # 视图
│ └─__init__.py # 内含工厂化函数
├─static  # 静态资源文件
├─templates  # 静态模板文件
├─test
│   └─ quqiadminflask.sql # 测试数据
├─.cz.yaml # commitizen配置文件
├─.env # 密钥文件
├─.flaskenv # flaskapp配置
├─.gitignore # git忽略文件
├─.pre-commit-config.yaml # pre-commit 配置文件
├─app.py # app文件
├─command.py # 自定义命令
├─flask_config.py # 配置文件
├─pyproject.toml # poetry配置文件
└─readme.md # 文档
```

## 配置

git clone之后
需要先创建虚拟环境

```shell
# 进入项目
cd quqi-admin-flask
# 如果没有poetry就先安装
pip install poetry
# 创建环境并安装包
poetry install
```

然后需要迁移数据库

```shell
flask db init
flask db migrate
flask db upgrade
```

导入测试数据

```shell
mysql -u 用户名 -p < ./test/quqiadminflask.sql
```

```shell
# 运行flask
flask run
```

## 贡献指南

如果想参与项目的贡献，提交代码之前需要启用 pre-commit、commitizen 对代码进行校验，运行以下指令即可。

初始化 pre-commit

```shell
pre-commit install
```

检查代码是否符合规范

```shell
git add .
pre-commit run --all-files
```

初始化 commitizen
使用 `cz commit` 代替 `git commit` 进行提交

并且需要格式化代码

```shell
isort .
black .
git add .
cz commit
git push
```