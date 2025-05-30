from datetime import date, time
from eh_app import db


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='appointments_as_doctor')
    patient = db.relationship('User', foreign_keys=[patient_id], backref='appointments_as_patient')
