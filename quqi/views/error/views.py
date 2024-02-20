from flask import current_app, jsonify, make_response, render_template

from quqi.extensions import csrf_protect
from quqi.views.error import error_bp


@error_bp.app_errorhandler(404)
def handle_404_error(e):
    current_app.logger.error(e)
    return render_template("errors/404.html"), 404


@error_bp.app_errorhandler(403)
def handle_403_error(e):
    current_app.logger.error(e)
    return render_template("errors/403.html"), 403


@error_bp.app_errorhandler(500)
def handle_404_error(e):
    current_app.logger.error(e)
    return render_template("errors/500.html"), 500


@error_bp.app_errorhandler(429)
def handle_429_error(e):
    current_app.logger.error(e)
    return render_template("errors/429.html"), 429


@error_bp.app_errorhandler(400)
def handle_400_error(e):
    current_app.logger.error(e)
    return render_template("errors/400.html"), 400
