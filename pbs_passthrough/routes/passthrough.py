from flask import Blueprint, render_template

bp = Blueprint("passthrough", __name__)

@bp.route("/passthrough")
def passthrough():
    return render_template("passthrough.html")