from dataclasses import dataclass

@dataclass
class TherapySession:
    _id: str
    session_id: str
    client_id: str
    doctor_id: str
    transcript: str