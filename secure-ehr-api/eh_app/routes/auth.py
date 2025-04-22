from flask import Blueprint, request, render_template, redirect, url_for
from eh_app.models.user import User
from eh_app import db
from sqlalchemy.exc import IntegrityError

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
