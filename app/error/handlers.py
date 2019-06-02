from flask import render_template
from app.errors import bp
from models import Model


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    Model.rollback()
    return render_template('errors/500.html'), 500
