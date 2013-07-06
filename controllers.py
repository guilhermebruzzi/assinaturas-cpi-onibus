#-*- coding:utf-8 -*-

from datetime import datetime
from mongoengine.queryset import DoesNotExist
from models import User, Meta
import uuid
#from config import redis_store
import json

def create_in_redis(**data):
    data["datetime_inscricao"] = str(data["datetime_inscricao"])
    return redis_store.set(data['user_id'] if data['user_id'] else data['facebook_id'], json.dumps(data))

def get_in_redis(user_id):
    return json.loads(redis_store.get(user_id))

def get_or_create_user(data):
    user_id = data['user_id'] if 'user_id' in data else None
    facebook_id = data['facebook_id'] if 'facebook_id' in data else None
    datetime_inscricao = datetime.now()
    city = None
    if "city" in data and data['city']:
        city = data['city']
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
#            user_from_redis = get_in_redis(user_id)
        except DoesNotExist:
            user = User.objects.create(user_id=user_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao, city=city)
#            user_from_redis = create_in_redis(user_id=user_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao, city=city)
    elif facebook_id:
        try:
            user = User.objects.get(facebook_id=facebook_id)
        except DoesNotExist:
            user = User.objects.create(facebook_id=facebook_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao, city=city)
#            user_from_redis = create_in_redis(facebook_id=facebook_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao, city=city)
    else:
        user_id = str(uuid.uuid4())
        user = User.objects.create(user_id=user_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao, city=city)
#        user_from_redis = create_in_redis(user_id=user_id, email=data['email'], name=data['name'], datetime_inscricao=datetime_inscricao, city=city)

    return user

def get_all_users_by_datetime():
    return User.objects.order_by('-datetime_inscricao')

def get_all_users_by_name():
    return User.objects.order_by('-name')

def get_meta():
    meta = Meta.objects.first()
    if not meta:
        meta = Meta()
        meta.maximo = 12000
        meta.save()
    return meta

def get_maximo_meta():
    meta = get_meta()
    return meta.maximo

def set_maximo_meta(maximo):
    meta = get_meta()
    meta.maximo = maximo
    meta.save()
