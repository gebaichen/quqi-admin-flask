from flask import render_template
from flask_login import login_required

from quqi.common.decorator import permission_required
from quqi.views.dashboard import dashboard_bp


# /dashboard/console
@dashboard_bp.get("/dashboard/console")
@login_required
@permission_required("dashboard:console")
def dashboard_console():
    return render_template("console.html")