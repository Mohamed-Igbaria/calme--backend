# services/session_service.py
from models.session import Session
from datetime import datetime



# Create a session
def create_session(
        date: datetime,
        gladia_id: str,
        title: str,
        note: str,
        patient_id: str,
        therapist_id: str
):
    session = Session(
        date=date,
        gladia_id=gladia_id,
        title=title,
        note=note,
        patient_id=patient_id,
        therapist_id=therapist_id
    )
    session.save()  # MongoEngine save
    return session


# Get all sessions
def get_all_sessions():
    return Session.objects.all()  # MongoEngine query all


# Get session by ID
def get_session_by_id(session_id):
    return Session.objects.get(id=session_id)  # MongoEngine query by id


# Get sessions by therapist ID with optional pagination and sorting
def get_sessions_by_therapist(
        therapist_id: str,
        limit: int = None,
        offset: int = None,
        order_desc: bool = True
):
    q = Session.objects(therapist_id=therapist_id)  # MongoEngine filter
    # Order by date
    if order_desc:
        q = q.order_by('-date')  # MongoEngine descending order
    else:
        q = q.order_by('date')  # MongoEngine ascending order

    # Pagination
    if offset is not None:
        q = q.skip(offset)
    if limit is not None:
        q = q.limit(limit)

    return q  # MongoEngine query result
