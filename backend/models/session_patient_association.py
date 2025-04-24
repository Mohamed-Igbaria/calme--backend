# models/session_patient_association.py
from sqlalchemy import Column, Integer, ForeignKey, Table
from extensions import db

session_patients = Table(
    'session_patients',
    db.Model.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True),
    Column('patient_id', Integer, ForeignKey('patients.id'), primary_key=True)
)
