from flask import render_template
from flask_login import login_required

from quqi.common.decorator import permission_required
from quqi.views.dashboard import dashboard_bp


@dashboard_bp.get("/")
@dashboard_bp.get("/dashboard")
@login_required
@permission_required("dashboard")
def dashboard_index():
    return render_template("index.html")
