from flask_restful import Api

from .apis import GiveRole, PowerAPI, RoleAPI, UserAPI, UserGiveRole


def register_dashboard_api(api_bp):
    # 集中注册 passport 下面的类视图
    # 最大的好处，方便管理，不需要关注每一个函数的细节
    dashboard_api = Api(api_bp)
    dashboard_api.add_resource(
        PowerAPI,
        "/dashboard/power",
        endpoint="dashboard_power",
        defaults={"p_id": None},
    )
    dashboard_api.add_resource(
        PowerAPI,
        "/dashboard/power/<int:p_id>",
        endpoint="dashboard_power_change",
    )
    dashboard_api.add_resource(
        RoleAPI, "/dashboard/role", endpoint="dashboard_role", defaults={"rid": None}
    )
    dashboard_api.add_resource(
        RoleAPI,
        "/dashboard/role/<int:rid>",
        endpoint="dashboard_role_change",
    )
    dashboard_api.add_resource(
        GiveRole,
        "/dashboard/role/power/<int:rid>",
        endpoint="dashboard_role_power",
    )
    dashboard_api.add_resource(
        UserAPI,
        "/dashboard/user",
        endpoint="dashboard_user",
        defaults={"user_id": None},
    )
    dashboard_api.add_resource(
        UserAPI, "/dashboard/user/<int:user_id>", endpoint="dashboard_change_user"
    )
    dashboard_api.add_resource(
        UserGiveRole,
        "/dashboard/user/role_user/<int:user_id>",
        endpoint="dashboard_change_user_role",
    )
    # dashboard_api.add_resource(
    #     dashboardContent, "/user/<int:user_id>/dashboard/<int:dashboard_id>", endpoint="dashboard_content"
    # )

    # rest full 风格的 api 服务器
    # 登录注册数据的操作
    # dashboard_api.add_resource(Login, "/passport/login", endpoint="login")
    # dashboard_api.add_resource(
    #     GetCaptcha, "/passport/getCaptcha", endpoint="get_captcha"
    # )
    # dashboard_api.add_resource(Logout, "/passport/logout", endpoint="logout")
