from flask import Blueprint, render_template, session, redirect
from flask import request
from eh_app.utils.security import decrypt_data

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

######################################################################
@main_bp.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    from eh_app.models.user import User

    user = User.query.get(session["user_id"])
    if user is None:
        return redirect("/login")

    # Desencriptar
    user.decrypt_fields()

    # Extraer campos desencriptados (evita re-acceso desde Jinja)
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "document_number": user.document_number,
        "birth_date": user.birth_date,
        "phone": user.phone,
        "address": user.address,
        "eps": user.eps,
        "blood_type": user.blood_type,
        "allergies": decrypt_data(user.allergies),
        "gender": user.gender,
        "role": user.role,
        "two_factor_enabled": user.two_factor_enabled
    }

    return render_template("profile.html", user=user_data)

# eh_app/routes/main.py

@main_bp.route("/schedule")
def schedule():
    if "user_id" not in session:
        return redirect("/login")

    from eh_app.models.user import User
    from eh_app.models.appointment import Appointment

    user = User.query.get(session["user_id"])

    if user.role == "doctor":
        appointments = Appointment.query.filter_by(doctor_id=user.id).all()
    elif user.role == "paciente":
        appointments = Appointment.query.filter_by(patient_id=user.id).all()
    else:  # admin
        appointments = Appointment.query.all()

    return render_template("schedule.html", user=user, appointments=appointments)


@main_bp.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    from eh_app.models.user import User

    user = User.query.get(session["user_id"])
    if user is None:
        return redirect("/login")

    if request.method == "POST":
        # Actualizar datos con lo que el usuario envía en el formulario
        user.full_name = request.form["full_name"]
        user.document_number = request.form["document_number"]
        user.address = request.form["address"]
        user.phone = request.form["phone"]
        user.email = request.form["email"]
        user.eps = request.form["eps"]
        user.birth_date = request.form["birth_date"]

        # Encriptar los campos antes de guardar (si aplica)
        user.encrypt_fields()

        # Guardar en la base de datos
        from eh_app import db
        db.session.commit()

        return redirect("/profile")

    # GET: mostrar formulario con los datos actuales
    user.decrypt_fields()
    return render_template("edit_profile.html", user=user)

@main_bp.route("/schedule")
def agenda():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("schedule.html")

@main_bp.route("/logout")
def logout():
    session.clear()  # Borra todos los datos de sesión
    return redirect("/")  # Redirige a la página de bienvenida o login
