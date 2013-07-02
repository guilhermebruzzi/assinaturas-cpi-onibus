#-*- coding:utf-8 -*-

from datetime import datetime
from mongoengine.queryset import DoesNotExist
from models import User
import uuid

def get_or_create_user(data):
    user_id = data['user_id'] if 'user_id' in data else None
    facebook_id = data['facebook_id'] if 'facebook_id' in data else None
    datetime_inscricao = datetime.now()
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except DoesNotExist:
            user = User.objects.create(user_id=user_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao)
    elif facebook_id:
        try:
            user = User.objects.get(facebook_id=facebook_id)
        except DoesNotExist:
            user = User.objects.create(facebook_id=facebook_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao)
    else:
        user_id = str(uuid.uuid4())
        user = User.objects.create(user_id=user_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao)

    if "city" in data and data['city'] and data['city'] != user.city:
        user.city = data['city']
        user.save()

    return user

def get_all_users_by_datetime():
    return User.objects.order_by('-datetime_inscricao')

def get_all_users_by_name():
    return User.objects.order_by('-name')
