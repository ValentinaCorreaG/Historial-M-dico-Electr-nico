from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template("welcome.html")
from flask import Blueprint, render_template, session, redirect

main_bp = Blueprint('main', __name__)

@main_bp.route("/dashboard")
def dashboard():
    # Requiere que el usuario haya iniciado sesión
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")
