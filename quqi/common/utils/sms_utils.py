import datetime


def send_sms_code(mobile, code):
    # 打印验证码
    content = f"""
    ---------------短信验证码------------------
    论坛正在测试~~~~
    手机号：{mobile}
    验证码：{code}
    时间：{datetime.datetime.now()}
    """
    return True
