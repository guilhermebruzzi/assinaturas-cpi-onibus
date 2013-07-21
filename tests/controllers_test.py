#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask

from datetime import datetime

from base_test import BaseTest

from models import User
from controllers import get_or_create_user
from config import redis_store

class ControllersTest(BaseTest):

    models = [User] #  A serem deletados a cada teste

    def setUp(self):
        super(ControllersTest, self).setUp()

        self.data_user_guilherme = { "name": "Guilherme Heynemann Bruzzi", "email": "guibruzzi@gmail.com", "bairro": "Leme", "celular": "(21) 8220-0093",
                                     'recaptcha_challenge_field' : 'test',
                                     'recaptcha_response_field' : 'test'}
        self.data_user_guto = { "name": "João Augusto Marrara Marzagão", "email": "gutomarzagao@gmail.com", "bairro": None, "celular": None,
                                'recaptcha_challenge_field' : 'test',
                                'recaptcha_response_field' : 'test' }


    def get_or_create_user_test(self):
        users = User.objects.all()
        self.assertEqual(len(users), 0)

        guilherme = get_or_create_user(self.data_user_guilherme)

        users = User.objects.all()
        self.assertEqual(len(users), 1)

        user_guilherme = users[0]

        self.assertEqual(guilherme, user_guilherme)

        self._assert_user(user=guilherme, user_data=self.data_user_guilherme)

        now = datetime.now()

        self.assertGreater(now, guilherme.datetime_inscricao)
        self.assertEqual(now.strftime("%Y-%m-%d %H:%M"), guilherme.datetime_inscricao.strftime("%Y-%m-%d %H:%M"))

        guilherme2 = get_or_create_user(data=self.data_user_guilherme)
        guilherme3 = get_or_create_user(data={"email": "guibruzzi@gmail.com"})

        self.assertEqual(guilherme2, guilherme)
        self.assertEqual(guilherme3, guilherme)


    def get_main_page_test(self):
        response = self._get_with_client("/")
        self.assert_template_used("index.html")
        self.assert200(response)
        self._assert_nome_completo_in_page(response)

    def get_main_page_logged_test(self):
        with self.client.session_transaction() as sess:
            sess['current_user'] = get_or_create_user(self.data_user_guilherme)

        response = self._get_with_client("/")
        self.assertRedirects(response, "/assinou/")

    def create_user_guto_test(self):
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        response = self._post_with_client(url="/", data=self.data_user_guto)
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        user_guto = users[0]
        self._assert_user(user=user_guto, user_data=self.data_user_guto)

    def create_user_guilherme_test(self):
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        response = self._post_with_client(url="/", data=self.data_user_guilherme)
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        user_guilherme = users[0]
        self._assert_user(user=user_guilherme, user_data=self.data_user_guilherme)

    def create_user_with_wrong_email_test(self):
        self.data_user_guilherme["email"] = "guibruzzi"
        data_erro = {'msg': u'Preencha um email válido.'}
        with self.app.test_client() as client: # necessario para manter a session ao retornar
            self._send_create_data(client, data_post=self.data_user_guilherme, data_erro=data_erro)


    def create_user_with_no_email_or_name_test(self):
        del self.data_user_guilherme["email"]
        data_erro = {'msg': u'Os campos "nome" e "email" são obrigatórios.'}

        with self.app.test_client() as client: # necessario para manter a session ao retornar
            self._send_create_data(client, data_post=self.data_user_guilherme, data_erro=data_erro)

            del self.data_user_guilherme["name"]
            self._send_create_data(client, data_post=self.data_user_guilherme, data_erro=data_erro)

            self.data_user_guilherme["email"] = "guibruzzi@gmail.com"
            self._send_create_data(client, data_post=self.data_user_guilherme, data_erro=data_erro)

    def create_user_with_wrong_captcha_test(self):
        self.data_user_guilherme["recaptcha_response_field"] = "wrong"
        data_erro = {'msg': u'Preencha corretamente o campo "texto da imagem".'}

        # Forcando a ter captcha
        self.app.config["TESTING"] = False
        redis_store.set('127.0.0.1', 3)

        with self.app.test_client() as client: # necessario para manter a session ao retornar
            self._send_create_data(client, data_post=self.data_user_guilherme, data_erro=data_erro)

        self.app.config["TESTING"] = True

