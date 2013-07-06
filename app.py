#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask, redirect, url_for, session, request, abort, make_response
from config import get_app, facebook
from helpers import render_template, need_to_be_logged, get_current_user, assinar_com_fb, assinar_com_dados
from controllers import get_all_users_by_datetime, set_maximo_meta, get_maximo_meta


app = get_app() #  Explicitando uma variável app nesse arquivo para o Heroku achar

@app.route('/', methods=['GET', 'POST'])
def index():
    current_user = get_current_user()
    if current_user:
#        current_user_in_redis = get_in_redis(current_user.user_id if current_user.user_id else current_user.facebook_id)
#        print current_user_in_redis
        return redirect(url_for('assinou'))

    if request.method == 'POST' and request.form and "name" in request.form and "email" in request.form:
        name = request.form["name"]
        email = request.form["email"]
        if name and email:
            assinar_com_dados(dados={"name": name, "email": email})
            return redirect(url_for('assinou'))
        else:
            return redirect(url_for('index'))

    maximo = get_maximo_meta()
    return render_template("index.html")

@app.route('/meta/<int:maximo>', methods=['GET', 'POST'])
def meta(maximo):
    current_user = get_current_user()
    all_users = get_all_users_by_datetime()
    if (current_user.name.startswith("Bernardo") and current_user.name.endswith("Ainbinder")) or\
        (current_user.name.startswith("Guilherme") and current_user.name.endswith("Bruzzi")):
        set_maximo_meta(maximo)
    else:
        maximo = get_maximo_meta()
    return render_template("meta.html", current_user=current_user, all_users=all_users, maximo=maximo)

@app.route('/assinou/', methods=['GET', 'POST'])
@need_to_be_logged
def assinou():
    current_user = get_current_user()
    all_users = get_all_users_by_datetime()
    ultimos_5 = all_users[:5]
    maximo = get_maximo_meta()

    return render_template("assinou.html", current_user=current_user, all_users=all_users, maximo=maximo, ultimos_5=ultimos_5)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    facebook_url = url_for('facebook_authorized', _external=True)
    return facebook.authorize(
        callback=facebook_url
    )

@app.route('/login/authorized/', methods=['GET', 'POST'])
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    oauth_token=resp['access_token']

    assinar_com_fb(oauth_token)

    return redirect(url_for('assinou'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
