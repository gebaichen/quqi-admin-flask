from flask import render_template
from flask_login import login_required

from quqi.common.decorator import permission_required
from quqi.models import RoleModel
from quqi.views.dashboard import dashboard_bp


@dashboard_bp.get("/dashboard/user")
@login_required
@permission_required("dashboard:system:user:read")
def dashboard_user():
    roles = RoleModel.query.all()
    return render_template("user.html", roles=roles)
