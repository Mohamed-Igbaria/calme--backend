
from mongoengine import Document, StringField, DateTimeField, ReferenceField



class Session(Document):
    date = DateTimeField(required=True)
    gladia_id = StringField(required=True)
    title = StringField(required=True)
    note = StringField()
    patient_id = StringField(required=True)
    therapist_id = StringField(required=True)

    meta = {
        'collection': 'sessions',  # MongoDB collection name
        'indexes': [
            'therapist_id',  # Add indexes for performance (optional)
        ]
    }
