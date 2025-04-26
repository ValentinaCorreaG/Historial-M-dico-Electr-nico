# migrate_data.py (ejecútalo una sola vez)
from eh_app import create_app, db
from eh_app.models.user import User
from eh_app.utils.security import encrypt_data

app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        try:
            # Encriptar solo si el campo no está en formato encriptado
            if user.full_name and not user.full_name.startswith('gAAAA'):
                user.full_name = encrypt_data(user.full_name)
            
            if user.document_number and not user.document_number.startswith('gAAAA'):
                user.document_number = encrypt_data(user.document_number)
            
            if user.address and not user.address.startswith('gAAAA'):
                user.address = encrypt_data(user.address)
            
            if user.allergies and not user.allergies.startswith('gAAAA'):
                user.allergies = encrypt_data(user.allergies)
            
            db.session.add(user)
        except Exception as e:
            print(f"Error con usuario ID {user.id}: {str(e)}")
            db.session.rollback()
    
    db.session.commit()
    print("Migración completada. Datos encriptados.")