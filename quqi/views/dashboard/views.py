from flask import render_template
from flask_login import login_required

from quqi.common.decorator import admin_required, permission_required
from quqi.models import RoleModel
from quqi.views.dashboard import dashboard_bp


@dashboard_bp.get("/")
@dashboard_bp.get("/dashboard")
@login_required
@permission_required("dashboard")
def dashboard_index():
    return render_template("index.html")


@dashboard_bp.get("/dashboard/role")
@login_required
@permission_required("dashboard:system:role:read")
def dashboard_role():
    return render_template("role.html")


@dashboard_bp.get("/dashboard/power")
@login_required
@permission_required("dashboard:system:power:read")
def dashboard_power():
    return render_template("power.html")


@dashboard_bp.get("/dashboard/user")
@login_required
@permission_required("dashboard:system:user:read")
def dashboard_user():
    roles = RoleModel.query.all()
    return render_template("user.html", roles=roles)


# /dashboard/console
@dashboard_bp.get("/dashboard/console")
@login_required
@permission_required("dashboard:console")
def dashboard_console():
    return render_template("console.html")
