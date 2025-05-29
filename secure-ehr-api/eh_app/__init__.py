from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from eh_app.routes.main import main_bp


# Extensiones globales
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object("eh_app.config.Config")  # Asegúrate de que esa ruta sea válida

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    # Importaciones locales dentro del contexto de la app
    with app.app_context():
        from eh_app.models.user import User  # Garantiza que el modelo se registre
        from eh_app.models.appointment import Appointment  # Garantiza que el modelo se registre 
        from eh_app.routes.auth import auth_bp
        from eh_app.routes.main import main_bp
        from eh_app.models.paciente import Paciente
        from eh_app.models.historia_clinica import HistoriaClinica  # Aquí


        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        

    return app
