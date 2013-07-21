#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask

from base_test import BaseTest
from models import User
from config import redis_store

class RedisTest(BaseTest):

    models = [User] #  A serem deletados a cada teste

    def setUp(self):
        super(RedisTest, self).setUp()
        self.data_user_guilherme = { "name": "Guilherme Heynemann Bruzzi", "email": "guibruzzi@gmail.com", "bairro": "Leme", "celular": "(21) 8220-0093",
                                     'recaptcha_challenge_field' : 'test',
                                     'recaptcha_response_field' : 'test'}

    def try_2_posts_1_get_test(self):
        self.app.config["TESTING"] = False

        with self.app.test_client() as client: # necessario para manter a session ao retornar
            for i in range(3):
                self._send_cookieless_create_user(client, redis_store, count_value=i+1, data_post=self.data_user_guilherme, url="/")

            with client.session_transaction() as sess:
                sess['current_user'] = None

            response = self._get_with_client("/", client)

            count = self._get_ip_count(redis_store)

            self.assertEqual(count, 3)

            self._assert_captcha_in_page(response)

        self.app.config["TESTING"] = True

    def try_3_posts_test(self):
        self.data_user_guilherme["recaptcha_response_field"] = "wrong"
        data_erro = {'msg': u'Preencha corretamente o campo "texto da imagem".'}

        self.app.config["TESTING"] = False

        with self.app.test_client() as client: # necessario para manter a session ao retornar
            for i in range(3):
                self._send_cookieless_create_user(client, redis_store, count_value=i+1, data_post=self.data_user_guilherme, url="/")

            with client.session_transaction() as sess:
                sess['current_user'] = None

            response = self._post_with_client(url="/", data=self.data_user_guilherme, client=client)

            self._assert_message(session=flask.session, data=data_erro, response=response)

            count = self._get_ip_count(redis_store)

            self.assertEqual(count, 4)

        self.app.config["TESTING"] = True
