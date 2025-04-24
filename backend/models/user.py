# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship
from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    sub = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    given_name = Column(String(255))
    family_name = Column(String(255))
    nickname = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    picture = Column(String(255))
    roles = Column(JSON)

    sessions_therapist = relationship('Session', back_populates='therapist', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.id} - {self.name}>'
