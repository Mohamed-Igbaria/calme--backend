# models/user.py
from mongoengine import Document, StringField, BooleanField, ListField
from datetime import datetime

class User(Document):
    sub = StringField(required=True, unique=True)
    name = StringField(required=True)
    given_name = StringField()
    family_name = StringField()
    nickname = StringField()
    email = StringField(required=True)
    email_verified = BooleanField(default=False)
    picture = StringField()  # This can be an ImageField or StringField depending on how you store images
    roles = ListField(StringField())

    meta = {
        'collection': 'users',  # MongoDB collection name
        'indexes': [
            'email',  # Optional, for better search performance on email
        ]
    }
