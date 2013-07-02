# -*- coding: utf-8 -*-

import os
import sys

from flask import Flask
from flaskext.oauth import OAuth
from flaskext.mongoengine import MongoEngine

def add_path():
    global project_root
    file_path = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath("%s/../" % file_path)
    sys.path.insert(0, project_root)
    return project_root

project_root = add_path()

def import_folder(folder_name, base_path = None):
    full_path = os.path.join(base_path, folder_name)
    folder = os.path.abspath(full_path)
    sys.path.insert(0, folder)


import_folder(folder_name='bands', base_path=project_root)

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

for key in app.config.keys():
    if os.environ.has_key(key):
        type_of_config = type(app.config[key])
        if type_of_config is bool:
            if os.environ[key] == "False":
                app.config[key] = False
            else:
                app.config[key] = True
        elif type_of_config is int:
            app.config[key] = int(os.environ[key])
        else:
            app.config[key] = os.environ[key]

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config["FACEBOOK_APP_ID"],
    consumer_secret=app.config["FACEBOOK_APP_SECRET"],
    request_token_params={'scope': 'email'}
)

db = MongoEngine(app)

def get_app():
    return app
