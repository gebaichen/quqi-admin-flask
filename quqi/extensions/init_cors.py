from flask_cors import CORS


def init_cors(app):
    CORS(app, resources=r"/*", supports_credentials=True)  # 使站点可以跨域提交cookie
