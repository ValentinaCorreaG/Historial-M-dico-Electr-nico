from eh_app import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    document_type = db.Column(db.String, nullable=False)
    document_number = db.Column(db.String, nullable=False, unique=True)
    birth_date = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    city = db.Column(db.String)
    blood_type = db.Column(db.String)
    allergies = db.Column(db.String)
    medical_history = db.Column(db.String)
    insurance = db.Column(db.String)
    occupation = db.Column(db.String)
    referred_by = db.Column(db.String)
    notes = db.Column(db.String)