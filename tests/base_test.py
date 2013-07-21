#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask

from flask.ext.testing import TestCase

from config import redis_store

class BaseTest(TestCase):

    def create_app(self):
        from config import get_app
        return get_app()

    def setUp(self):
        self._delete_all() #  Chama a funcao que deleta todos os models que essa classe testa

    def tearDown(self):
        self._delete_all()

    def _delete_all(self):
        redis_store.flushall()
        for model in self.models:
            self._delete_all_of_a_model(model)

    def _delete_all_of_a_model(self, model):
        model.drop_collection()

    def _assert_text_in_page(self, text, page):
        self.assertIn(text, page.data)

    def _assert_nome_completo_in_page(self, main_page):
        self._assert_text_in_page(text='<label class="label-form" for="name">Nome completo <small>*</small></label>', page=main_page)

    def _assert_captcha_in_page(self, main_page):
        self._assert_text_in_page(text='<script type="text/javascript">var RecaptchaOptions = {"lang": "pt",', page=main_page)

    def _assert_message_in_page(self, data, main_page):
        aspas_txt = '"'
        aspas_html = '&#34;'

        msg = data['msg']

        if aspas_txt in msg:
            msg = msg.replace(aspas_txt, aspas_html)

        self._assert_text_in_page(text=msg, page=main_page)

    def _assert_user(self, user, user_data):
        keys = ["name", "email", "celular", "bairro"]
        for key in keys:
            if key in user_data and not user_data[key] == None:
                val_obj = getattr(user, key)
                val_data = user_data[key]
                self.assertEqual(val_obj, val_data)

    def _assert_message(self, session, data, response, url_redirected="/"):
        self.assertRedirects(response, url_redirected)
        self.assertIn("msg", session)
        self.assertEqual(session["msg"], data["msg"])

    def _get_ip_count(self, redis_store):
        ip = redis_store.keys()[0]
        count = int(redis_store.get(ip))
        return count

    def _get_with_client(self, url, client=None):
        if not client:
            client = self.client
        return client.get(url, environ_base={'REMOTE_ADDR': '127.0.0.1'})

    def _post_with_client(self, url, data, client=None):
        if not client:
            client = self.client
        return client.post(url, data=data, environ_base={'REMOTE_ADDR': '127.0.0.1'})

    def _send_cookieless_create_user(self, client, redis_store, count_value, data_post, url="/"):
        with client.session_transaction() as sess:
            sess['current_user'] = None

        response = self._post_with_client(url, data_post, client)

        count = self._get_ip_count(redis_store)

        self.assertEqual(count, count_value)
        self.assertRedirects(response, "/assinou/")
        self._assert_user(flask.session['current_user'], data_post)

    def _send_create_data(self, client, data_post, data_erro, url="/"):
        response = self._post_with_client(url, data_post, client)
        self._assert_message(session=flask.session, data=data_erro, response=response)

        main_page = self._get_with_client("/", client)
        self._assert_message_in_page(data_erro, main_page)

        self.assertNotIn("msg", flask.session)
