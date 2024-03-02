from flask import current_app, request
from flask_restful import Resource

from quqi.common.returns import return_error_api, return_success_api
from quqi.common.utils.file_utils import save_pic
from quqi.common.utils.response_code import RET


class UploadImage(Resource):
    def post(self):
        file = request.files.get("file")
        if not file:
            return return_error_api(code=RET.header_data_is_small, msg="没有数据")
        try:
            filename = file.filename
            content = file.read()
        except Exception as e:
            current_app.logger.error(e)
            return return_error_api(code=RET.header_data_error, msg="数据提取失败")
        if not all([filename, content]):
            return return_error_api(
                code=RET.header_data_is_small,
                msg="没有数据提取的结果",
            )
        img_url = save_pic(filename, content)
        if not img_url:
            return return_error_api(code=RET.commit_error, msg="图片保存失败")
        return return_success_api(
            code=RET.ok,
            msg="图片上传成功",
            image_url=img_url,
            location=img_url,
        )
