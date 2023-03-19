import time
import sys
import json
import redis
import requests
import logging

from faker import Faker

sys.path.insert(0, '../')

logging.basicConfig(filename='marketing.log', encoding='utf-8', level=logging.INFO)

## Configuración Login
URL_LOGIN ='http://127.0.0.1:5001/login'
URL_OBTENER_CANAL ='http://127.0.0.1:5001/api/canales'
USUARIO_AUTORIZADOR = { "usuario": "cliente1", "contrasena": "cliente1"}

## Configuración queue marketing
CANAL_OFERTAS = 'marketing_ofertas'
REDIS_CONNECTION = redis.Redis(host='localhost', port=6379, db=0)

redis_db = REDIS_CONNECTION
sub = redis_db.pubsub()

class Handler():
    @staticmethod
    def escuchar():
        
        # Obtiene token autorizador
        login = requests.post(URL_LOGIN, json = USUARIO_AUTORIZADOR)
        if login.status_code != 200:
            logging.error('Error al intentar autenticar componente marketing http code', login.status_code)
            return
        respLogin = json.loads(login.content.decode('utf-8'))
        
        if 'error' in respLogin:
            logging.error('Error al intentar autenticar componente marketing - ' + respLogin['error'])
            return
        else:
            token = respLogin['data']

        # Obtiene canal marketing para escuchar peticiones
        respCanal = requests.get(URL_OBTENER_CANAL, headers = {"Authorization": 'Bearer ' + token})
        if respCanal.status_code != 200:
            logging.error('Error al intentar obtener el canal autorizado para crear ofertas')
            return
        canal_marketing = json.loads(respCanal.content.decode('utf-8'))['data']

        print('Escuchando mensajes del canal', canal_marketing)
        sub.subscribe(canal_marketing)
        Handler.leer_mensajes()

    @staticmethod
    def leer_mensajes():
        while True:
            mensaje = sub.get_message()
            if mensaje and type(mensaje['data']) is bytes:
                oferta = json.loads(mensaje['data'].decode('utf-8'))
                oferta['ofertaId'] = Faker().uuid4()
                oferta['ofertaEstado'] = 'CREADA'
                print('Oferta creada!', oferta)
                logging.info('Oferta creada' + json.dumps(oferta))
                redis_db.publish(CANAL_OFERTAS, json.dumps(oferta))
                
            time.sleep(0.01)
