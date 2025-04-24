# models/session.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from extensions import db
from models.session_patient_association import session_patients

class Session(db.Model):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    title = Column(String(255), nullable=False)
    note = Column(Text)

    therapist_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    therapist = relationship('User', back_populates='sessions_therapist')

    patients = relationship('Patient', secondary=session_patients, back_populates='sessions')

    transcription_data = Column(JSON)
    analysis_data = Column(JSON)
    top_words=Column(JSON)

    def __repr__(self):
        return f'<Session {self.id} - {self.title}>'
