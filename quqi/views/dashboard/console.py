import psutil
from flask import render_template
from flask_login import login_required

from quqi.common.decorator import permission_required
from quqi.views.dashboard import dashboard_bp


# /dashboard/console
@dashboard_bp.get("/dashboard/console")
@login_required
@permission_required("dashboard:console")
def dashboard_console():
    # cpu使用率
    cpus_percent = psutil.cpu_percent(interval=0.1, percpu=False)  # percpu 获取主使用率
    memory = psutil.virtual_memory()
    memory_percent = memory.percent  # 内存占用率
    return render_template(
        "console.html", cpus_percent=cpus_percent, memory_percent=memory_percent
    )
