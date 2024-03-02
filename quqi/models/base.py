from datetime import datetime

from flask import current_app

from quqi.common.returns import return_error_api, return_success_api
from quqi.common.utils.response_code import RET
from quqi.extensions import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_at = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # 记录的更新时间

    def save_add_db(self):
        db.session.add(self)
        db.session.commit()

    def save_delete_db(self):
        db.session.delete(self)
        db.session.commit()
