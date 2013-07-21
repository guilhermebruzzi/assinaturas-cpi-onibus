# -*- coding: utf-8 -*-

import os
import sys

from flask import Flask
from flaskext.oauth import OAuth
from flaskext.mongoengine import MongoEngine
from flask_redis import Redis
from flask.ext.cache import Cache

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

cache = Cache(app)

redis_store = Redis(app)

BAIRROS = [
    u"Bairro Imperial de São Cristóvão", u"Benfica", u"Caju", u"Catumbi", u"Centro", u"Cidade Nova", u"Estácio", u"Gamboa", u"Glória", "Lapa", "Mangueira", u"Paquetá", "Rio Comprido", "Santa Teresa", "Santo Cristo", u"Saúde", "Vasco da Gama",
    "Botafogo", "Catete", "Copacabana", "Cosme Velho", "Flamengo", u"Gávea", u"Humaitá", "Ipanema", u"Jardim Botânico", "Lagoa", "Laranjeiras", "Leblon", "Leme", "Rocinha", u"São Conrado", "Urca", "Vidigal",
    "Anil", "Barra da Tijuca", "Barra de Guaratiba", "Camorim", "Cidade de Deus", "Curicica", u"Freguesia de Jacarepaguá", u"Gardênia Azul", "Grumari", u"Itanhangá", u"Jacarepaguá", u"Joá", u"Praça Seca", "Pechincha", "Recreio dos Bandeirantes", "Tanque", "Taquara", "Vargem Grande", "Vargem Pequena", "Vila Valqueire",
    "Bangu", "Campo Grande", "Cosmos", "Deodoro", "Ecoville", "Guaratiba", u"Inhoaíba", "Jardim Sulacap", u"Magalhães Bastos", "Paciencia", "Padre Miguel", "Pedra de Guaratiba", "Realengo", "Santa Cruz", u"Santíssimo", u"Senador Camará", "Senador Vasconcelos", "Sepetiba", "Vila Militar",
    "Alto da Boa Vista", u"Andaraí", u"Grajaú", u"Maracanã", u"Praça da Bandeira", "Tijuca", "Vila Isabel",
    u"Bancários", "Cacuia", u"Cidade Universitária", u"Cocotá", "Freguesia", u"Galeão", "Jardim Carioca", "Jardim Guanabara", u"Moneró", "Pitangueiras", "Portuguesa", "Praia da Bandeira", "Ribeira", u"Tauá", "Zumbi",
    u"Abolição", u"Agua Santa", "Acari", "Anchieta", "Barros Filho", "Bento Ribeiro", "Bonsucesso", u"Brás de Pina", "Cachambi", "Cavalcante", "Campinho", "Cascadura", "Coelho Neto", u"Colégio", u"Complexo do Alemão", "Cordovil", "Costa Barros", "Del Castilho", "Encantado", "Engenheiro Leal", "Engenho da Rainha", "Engenho de Dentro", "Engenho Novo", "Guadalupe", u"Higienópolis", u"Honório Gurgel", u"Irajá", u"Inhaúma", u"Jacaré", "Jacarezinho", u"Jardim América", "Lins de Vasconcelos", "Madureira", "Manguinhos", u"Maré", "Marechal Hermes", u"Maria da Graça", u"Méier", "Olaria", "Oswaldo Cruz", "Parada de Lucas", "Parque Anchieta", u"Parque Colúmbia", "Pavuna", "Penha", "Penha Circular", "Piedade", "Pilares", "Quintino Bocaiuva", "Ramos", "Riachuelo", "Ricardo de Albuquerque", "Rocha", "Rocha Miranda", "Sampaio", u"São Francisco Xavier", u"Tomás Coelho", u"Turiaçu", "Vaz Lobo", "Vicente de Carvalho", u"Vigário Geral", "Vila da Penha", "Vila Kosmos", "Vista Alegre"
]

BAIRROS = sorted(BAIRROS)

def get_app():
    return app
