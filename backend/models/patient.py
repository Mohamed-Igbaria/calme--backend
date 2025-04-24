# models/patient.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from extensions import db

class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String)
    age = Column(Integer)
    gender = Column(String)

    sessions = relationship('Session', secondary='session_patients', back_populates='patients')

    def __repr__(self):
        return f'<Patient {self.id} - {self.full_name}>'
