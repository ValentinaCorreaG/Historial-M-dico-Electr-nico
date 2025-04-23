from flask import Blueprint, render_template, session, redirect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template("welcome.html")


@main_bp.route("/dashboard")
def dashboard():
    # Requiere que el usuario haya iniciado sesión
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

@main_bp.route("/profile")
def perfil():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("profile.html")

@main_bp.route("/schedule")
def agenda():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("schedule.html")

@main_bp.route("/logout")
def logout():
    session.clear()  # Borra todos los datos de sesión
    return redirect("/")  # Redirige a la página de bienvenida o login
