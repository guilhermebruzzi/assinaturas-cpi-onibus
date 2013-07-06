# -*- coding: utf-8 -*-

import re
from datetime import datetime
from mongoengine import *
from config import db

lastfm = None
controllers_module = None

class User(db.Document):
    facebook_id = db.StringField(required=False)
    user_id = db.StringField(required=False)
    email = db.StringField(required=True)
    name = db.StringField(required=True)
    city = db.StringField(required=False)
    datetime_inscricao = db.DateTimeField(required=True)

    @property
    def photo(self):
        if self.facebook_id:
            url = 'http://graph.facebook.com/%s/picture'
            return url % self.facebook_id
        return '/static/images/cpi.jpg'

    def __eq__(self, other):
        return self.email == other.email

    def __unicode__(self):
        return self.name

class Meta(db.Document):
    maximo = db.IntField(required=True)
