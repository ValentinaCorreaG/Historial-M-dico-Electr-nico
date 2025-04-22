from flask import Blueprint, request, render_template, redirect, url_for
from eh_app.models.user import User
from eh_app import db
from sqlalchemy.exc import IntegrityError
from eh_app.utils.email import enviar_codigo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            form = request.form

            # Crear usuario
            user = User(
                username=form.get("email").split('@')[0],  # o un campo separado
                email=form.get("email"),
                full_name=form.get("full_name"),
                document_number=form.get("document_number"),
                birth_date=form.get("birth_date"),
                address=form.get("address"),
                phone=form.get("phone"),
                eps=form.get("eps"),
                blood_type=form.get("blood_type"),
                allergies=form.get("allergies"),
                gender=form.get("gender"),
                role="paciente"
            )

            user.set_password(form.get("password"))
            user.encrypt_fields()

            db.session.add(user)
            db.session.commit()

            return render_template("register.html", success="Registro exitoso. Ya puedes iniciar sesión.")
        except IntegrityError:
            db.session.rollback()
            return render_template("register.html", error="El correo ya está registrado.")
        except Exception as e:
            return render_template("register.html", error=f"Ocurrió un error: {str(e)}")

    return render_template("register.html")

from flask import jsonify
from eh_app.models.user import User

@auth_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = User.query.all()
    datos = []
    for u in usuarios:
        try:
            u.decrypt_fields()
        except Exception:
            pass  # por si algún campo no se puede descifrar

        datos.append({
            "email": u.email,
            "rol": u.role,
            "nombre": u.full_name,
            "documento": u.document_number
        })
    return jsonify(datos)

import random
from flask import session
from eh_app.models.user import User
from eh_app.utils.email import enviar_codigo

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print("[DEBUG] Email ingresado:", email)
        print("[DEBUG] Password ingresado:", password)

        user = User.query.filter_by(email=email).first()
        if not user:
            print("[ERROR] Usuario no encontrado.")
            return render_template("login.html", error="Usuario no encontrado")

        print("[DEBUG] Usuario encontrado:", user.email)

        if not user.check_password(password):
            print("[ERROR] Contraseña incorrecta para:", user.email)
            return render_template("login.html", error="Contraseña incorrecta")

        print("[DEBUG] Contraseña correcta. 2FA habilitado:", user.two_factor_enabled)

        if user.two_factor_enabled:
            codigo = f"{random.randint(100000, 999999)}"
            print("[DEBUG] Código generado:", codigo)
            user.two_factor_code = codigo
            db.session.commit()
            enviar_codigo(user.email, codigo)
            print("[DEBUG] Código enviado a:", user.email)

            session["2fa_user_id"] = user.id
            return redirect(url_for("auth.verify_2fa"))

        session["user_id"] = user.id
        session["rol"] = user.role
        return redirect("/dashboard")

    return render_template("login.html")


@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if request.method == "POST":
        codigo = request.form.get("codigo")
        user_id = session.get("2fa_user_id")
        user = User.query.get(user_id)

        if user and user.two_factor_code == codigo:
            user.two_factor_code = None
            db.session.commit()
            session["user_id"] = user.id
            session["rol"] = user.role
            return redirect("/dashboard")
        return render_template("verify_2fa.html", error="Código inválido")

    return render_template("verify_2fa.html")
