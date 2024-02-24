from flask_assets import Bundle, Environment

assets = Environment()

passport_js = Bundle(
    "js/cookie.js", "layui/layui.js", filters="jsmin", output="dist/passport_js.js"
)

assets.register("passport_js", passport_js)

passport_css = Bundle(
    "layui/css/layui.css",
    "css/passport.css",
    filters="cssmin",
    output="dist/passport_css.css",
)

assets.register("passport_css", passport_css)

index_css = Bundle(
    "layui/css/layui.css",
    filters="cssmin",
    output="dist/index_css.css",
)
index_js = Bundle(
    "js/cookie.js", "layui/layui.js", filters="jsmin", output="dist/index_js.js"
)
assets.register("index_css", index_css)
assets.register("index_js", index_js)

dashboard_js = Bundle(
    "layui/layui.js",
    "js/cookie.js",
    filters="jsmin",
    output="dist/dashboard_js.js",
)

assets.register("dashboard_js", dashboard_js)

dashboard_css = Bundle(
    "layui/css/layui.css",
    "layuiadmin/style/admin.css",
    filters="cssmin",
    output="dist/dashboard_css.css",
)
assets.register("dashboard_css", dashboard_css)
dashboard_profiles_css = Bundle(
    "layui/css/layui.css",
    "layuiadmin/style/admin.css",
    "layuiadmin/style/template.css",
    filters="cssmin",
    output="dist/dashboard_profiles_css.css",
)
assets.register("dashboard_profiles_css", dashboard_profiles_css)


def init_assets(app):
    assets.init_app(app)
