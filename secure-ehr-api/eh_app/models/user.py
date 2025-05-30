from werkzeug.security import generate_password_hash, check_password_hash
from eh_app.utils.security import encrypt_data, decrypt_data
from eh_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='paciente', nullable=False)

    # Campos encriptados
    full_name = db.Column(db.Text, nullable=False)
    document_number = db.Column(db.Text, nullable=False)
    birth_date = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    eps = db.Column(db.String(50))
    blood_type = db.Column(db.String(5))
    allergies = db.Column(db.Text)
    gender = db.Column(db.String(10))

    # Campos para 2FA
    two_factor_enabled = db.Column(db.Boolean, default=True)
    two_factor_code = db.Column(db.String(6), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encrypt_fields(self):
        self.full_name = encrypt_data(self.full_name)
        self.document_number = encrypt_data(self.document_number)
        if self.address:
            self.address = encrypt_data(self.address)
        if self.allergies:
            self.allergies = encrypt_data(self.allergies)

    def decrypt_fields(self):
        try:
            self.full_name = decrypt_data(self.full_name) if self.full_name else None
        except:
            pass  # Mantener el valor original si no se puede desencriptar
        
        try:
            self.document_number = decrypt_data(self.document_number) if self.document_number else None
        except:
            pass
        
        if self.address:
            try:
                self.address = decrypt_data(self.address)
            except:
                pass
        
        if self.allergies:
            try:
                self.allergies = decrypt_data(self.allergies)
            except:
                pass