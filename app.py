#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask, redirect, url_for, session, request, abort, make_response

from config import get_app, facebook, BAIRROS, cache
from helpers import render_template, need_to_be_logged, get_current_user, assinar_com_fb, assinar_com_dados
from controllers import get_all_users_by_datetime, set_maximo_meta, get_maximo_meta, get_redis_count, incr_redis_count
from forms import UserCaptchaForm, UserForm

app = get_app() #  Explicitando uma variável app nesse arquivo para o Heroku achar
user_form_default = UserForm()
user_captcha_form_default = UserCaptchaForm()


@cache.cached(timeout=18000)
def pagina_principal():
    return render_template("index.html", BAIRROS=BAIRROS, msg=None, form=user_form_default)

def get_form():
    count = get_redis_count(request)

    if count:
        count = int(count)
    else:
        count = 0

    if request.method == 'POST':
        form = UserForm(request.form) if count <= 2 else UserCaptchaForm(request.form)
    else:
        form = user_form_default if count <= 2 else user_captcha_form_default

    return form

@app.route('/', methods=['GET', 'POST'])
def index():
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('assinou'))

    msg = session['msg'] if 'msg' in session else None

    form = get_form()

    if request.method == 'GET' and not msg and not isinstance(form, UserCaptchaForm):
        return pagina_principal()

    if msg:
        del session['msg']

    if request.method == 'POST':
        incr_redis_count(request)
        name = request.form.get("name")
        email = request.form.get("email")
        celular = request.form.get("celular")
        bairro = request.form.get("bairro")
        if form.validate():
            assinar_com_dados(dados={"name": name, "email": email, "bairro": bairro, "celular": celular})
            return redirect(url_for('assinou'))
        else:
            if not name or not email:
                session['msg'] = u'Os campos "nome" e "email" são obrigatórios.'
            elif hasattr(form, "captcha") and len(form.captcha.errors) > 0:
                session['msg'] = u'Preencha corretamente o campo "texto da imagem".'
            elif email and len(form.email.errors) > 0:
                session['msg'] = u'Preencha um email válido.'
            else:
                session['msg'] = u'Preencha corretamente os campos abaixo.'

            return redirect(url_for('index'))

    return render_template("index.html", BAIRROS=BAIRROS, msg=msg, form=form)

def __make_response_plain_text__(response_text, type_of_response="text/plain"):
    response = make_response(response_text)
    response.headers["Content-type"] = type_of_response
    return response

@app.route('/lista-assinaturas.csv', methods=['GET'])
def lista_inscritos():
    csv_lista_assinantes = "nome, email, celular, bairro, datetime_inscricao\n"
    all_users = get_all_users_by_datetime()
    for user in all_users:
        csv_lista_assinantes += "%s, %s, %s, %s, %s\n" % (user.name, user.email, user.celular, user.bairro, str(user.datetime_inscricao))
    return __make_response_plain_text__(csv_lista_assinantes)


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
