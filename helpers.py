#-*- coding:utf-8 -*-

import unicodedata
import re
import flask
import json
import urllib2
import random

from flask import session, render_template, request
from config import get_app
from controllers import get_or_create_user

facebook_module = None
app = get_app()

def render_template(url, **data):
    if not "debug" in data.keys():
        data["debug"] = app.config["DEBUG"]
        data["app_id"] = app.config["FACEBOOK_APP_ID"]

    return flask.render_template(url, **data)

def get_client_ip():
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return ip

def get_slug(title):
    slug = unicodedata.normalize('NFKD', unicode(title))
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

def get_json(url):
    response = urllib2.urlopen(url)
    json_response = json.loads(response.read())
    return json_response

def random_insert(elm, lista):
    tamanho = len(lista)
    indice = random.randint(0, tamanho)
    lista.insert(indice, elm)
    return lista


def user_logged():
    return ('current_user' in flask.session.keys())

def get_current_user():
    if user_logged():
        return session['current_user']
    else:
        return None

def need_to_be_logged(handler, path="/"):
    def wrapper(*args, **kwargs):
        if not user_logged():
            return flask.redirect(path)
        return handler(*args, **kwargs)

    wrapper.__name__ = handler.__name__
    return wrapper

def assinar_com_fb(oauth_token):
    global facebook_module, controllers_module

    session['oauth_token'] = (oauth_token, '')

    if not facebook_module:
        facebook_module = __import__("facebook")

    me_data = facebook_module.get_facebook_data(oauth_token)

    city = me_data['location']['name'] if 'location' in me_data and 'name' in me_data['location'] else None
    me_data['city'] = city.split(',')[0] if city and ',' in city else city

    session['current_user'] = get_or_create_user(me_data)

def assinar_com_dados(dados):
    session['current_user'] = get_or_create_user(dados)
