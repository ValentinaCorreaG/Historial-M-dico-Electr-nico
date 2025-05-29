# eh_app/models/historia_clinica.py

from eh_app import db
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON  

class HistoriaClinica(db.Model):
    __tablename__ = 'historias_clinicas'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    record_date = db.Column(db.Date, default=datetime.utcnow)
    reason = db.Column(db.String, nullable=False)
    blood_pressure = db.Column(db.String)
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    oxygen_saturation = db.Column(db.Integer)
    diagnosis = db.Column(db.String, nullable=False)
    diagnosis_details = db.Column(db.Text)
    treatment = db.Column(db.Text)
    medications = db.Column(JSON, nullable=True)  # Lista de objetos con nombre y dosis
    observations = db.Column(db.Text)

    paciente = db.relationship('Paciente', backref='historias_clinicas', lazy=True)
