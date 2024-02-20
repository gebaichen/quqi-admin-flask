from datetime import datetime

from flask import Flask

import quqi.models as models
from quqi.extensions import db


def register_command(app: Flask):
    @app.cli.command()
    def create_role():
        roles = [
            {"name": "普通用户", "code": "user"},
            {"name": "管理员", "code": "admin"},
            {"name": "超级管理员", "code": "super-admin"},
        ]

        role1 = models.RoleModel(name=roles[0]["name"], code=roles[0]["code"])
        role2 = models.RoleModel(name=roles[1]["name"], code=roles[1]["code"])
        role3 = models.RoleModel(name=roles[2]["name"], code=roles[2]["code"])
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.commit()

    @app.cli.command()
    def user():
        from quqi.models import UserModel
        user = UserModel()
        user.username = 'quqi'
        user.set_password_hash('123456')
        user.role_id = 3
        user.save_add_db()

