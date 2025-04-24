from models.user import User
from app import db
from sqlalchemy.exc import IntegrityError


def create_user(data):
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
    db.session.add(user)
    try:
        db.session.commit()
        return user
    except IntegrityError:
        db.session.rollback()
        raise ValueError('Email must be unique')


# جلب كل المستخدمين
def get_all_users():
    return User.query.all()


# جلب مستخدم حسب sub
def get_user_by_id(sub):
    return User.query.filter_by(sub=sub).first()


# جلب أو إنشاء مستخدم
def get_or_create_user(user_payload):
    sub = user_payload.get('sub')
    user = User.query.filter_by(sub=sub).first()

    if user:
        return user

    new_user = User(
        sub=sub,
        name=user_payload.get('name'),
        given_name=user_payload.get('given_name'),
        family_name=user_payload.get('family_name'),
        nickname=user_payload.get('nickname'),
        email=user_payload.get('email'),
        email_verified=user_payload.get('email_verified', False),
        picture=user_payload.get('picture'),
        roles=user_payload.get('https://chatbot.example.com/roles', [])
    )
    db.session.add(new_user)
    try:
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Email must be unique")
