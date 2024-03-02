from datetime import datetime

from flask import session
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from quqi.extensions import db
from quqi.models.base import BaseModel


class UserModel(BaseModel, db.Model, UserMixin):
    """用户表"""

    __tablename__ = "info_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    username = db.Column(
        db.String(32), unique=True, nullable=False, comment="用户昵称"
    )  # 用户昵称
    avatar = db.Column(
        db.String(255), comment="头像", default="/static/images/user_pic.png"
    )
    email = db.Column(db.String(40), unique=True, comment="用户邮箱")
    address = db.Column(db.String(255), comment="用户地址")
    mobile = db.Column(db.String(11), unique=True, nullable=False, comment="用户手机号")
    password_hash = db.Column(
        db.String(255), nullable=False, comment="加密的密码"
    )  # 加密的密码
    role_id = db.Column(db.Integer, db.ForeignKey("rt_role.id"))

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def check_p(self, p):
        p_ = [power.code for power in self.role.power]
        if p in p_:
            return True
        else:
            return False

    def check_r(self, r):
        role = self.role
        if r == role.code:
            return True
        else:
            return False


# 创建中间表
role_power = db.Table(
    "rt_role_power",  # 中间表名称
    db.Column(
        "power_id", db.Integer, db.ForeignKey("rt_power.id"), comment="用户编号"
    ),  # 属性 外键
    db.Column(
        "role_id", db.Integer, db.ForeignKey("rt_role.id"), comment="角色编号"
    ),  # 属性 外键
)


class RoleModel(BaseModel, db.Model):
    __tablename__ = "rt_role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, comment="角色名称")
    code = db.Column(db.String(64), unique=True, comment="角色标识")
    users = db.relationship("UserModel", backref="role", lazy="dynamic")
    power = db.relationship(
        "PowerModel", secondary="rt_role_power", backref=db.backref("role")
    )

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
        }


class PowerModel(BaseModel, db.Model):
    __tablename__ = "rt_power"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment="权限名字")
    url = db.Column(db.String(64), comment="权限路径")
    code = db.Column(db.String(64), comment="权限标识")
    type = db.Column(db.String(30), comment="权限类型")
    pid = db.Column(db.Integer, db.ForeignKey("rt_power.id"), comment="父类编号")
    sort = db.Column(db.Integer, default=1)
    parent = db.relationship(
        "PowerModel", backref=db.backref("children", lazy="dynamic"), remote_side=[id]
    )

    # children = db.relationship("PowerModel", back_populates="parent", lazy="dynamic")

    def json(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "url": self.url,
            "pid": self.pid,
            "sort": self.sort,
            "type": self.type,
        }
