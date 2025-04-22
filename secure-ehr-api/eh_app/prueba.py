@auth_bp.route("/usuarios")
def listar_usuarios():
    from eh_app.models.user import User
    usuarios = User.query.all()
    return {
        "usuarios": [
            {"email": u.email, "rol": u.role, "nombre": u.full_name}
            for u in usuarios
        ]
    }
