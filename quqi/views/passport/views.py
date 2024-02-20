from flask import render_template
from flask_wtf.csrf import generate_csrf

from quqi.views.passport import passport_bp


@passport_bp.get("/passport/login")
def login():
    return render_template("login.html")


@passport_bp.after_app_request
def after_request(response):
    response.set_cookie("csrf-token", generate_csrf())
    return response
