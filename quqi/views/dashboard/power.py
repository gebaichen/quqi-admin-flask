from flask import render_template
from flask_login import login_required

from quqi.common.decorator import permission_required
from quqi.views.dashboard import dashboard_bp


@dashboard_bp.get("/dashboard/power")
@login_required
@permission_required("dashboard:system:power:read")
def dashboard_power():
    return render_template("power.html")
