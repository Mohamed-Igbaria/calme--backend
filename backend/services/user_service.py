# services/user_service.py
from models.user import User

from mongoengine.errors import NotUniqueError, DoesNotExist



def create_user(data):
    try:
        user = User(
            sub=data.get('sub'),
            name=data.get('name'),
            given_name=data.get('given_name'),
            family_name=data.get('family_name'),
            nickname=data.get('nickname'),
            email=data.get('email'),
            email_verified=data.get('email_verified', False),
            picture=data.get('picture'),
            roles=data.get('roles', [])
        )
        user.save()
        return user
    except NotUniqueError:
        raise ValueError('Email must be unique')



def get_all_users():
    return User.objects.all()



def get_user_by_id(sub):
    try:
        return User.objects.get(sub=sub)
    except DoesNotExist:
        return None


# Function to get or create a user
def get_or_create_user(user_payload):
    sub = user_payload.get('sub')
    email = user_payload.get('email')

    try:
        user = User.objects.get(sub=sub)
        return user
    except DoesNotExist:
        try:
            user = User(
                sub=sub,
                name=user_payload.get('name'),
                given_name=user_payload.get('given_name'),
                family_name=user_payload.get('family_name'),
                nickname=user_payload.get('nickname'),
                email=email,
                email_verified=user_payload.get('email_verified', False),
                picture=user_payload.get('picture'),
                roles=user_payload.get('https://chatbot.example.com/roles', [])
            )
            user.save()
            return user
        except NotUniqueError:
            raise ValueError("Email must be unique")