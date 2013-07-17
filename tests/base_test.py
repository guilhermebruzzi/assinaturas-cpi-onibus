#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.testing import TestCase

class BaseTest(TestCase):

    def create_app(self):
        from config import get_app
        return get_app()

    def setUp(self):
        self._delete_all() #  Chama a funcao que deleta todos os models que essa classe testa

    def tearDown(self):
        self._delete_all()

    def _delete_all(self):
        for model in self.models:
            self._delete_all_of_a_model(model)

    def _delete_all_of_a_model(self, model):
        model.drop_collection()

    def _assert_text_in_page(self, text, page):
        self.assertIn(text, page.data)

    def _assert_nome_completo_in_page(self, main_page):
        self._assert_text_in_page(text='<label class="label-form" for="name">Nome completo <small>*</small></label>', page=main_page)

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
