import time
import sys
import json
import redis
import requests

from faker import Faker

sys.path.insert(0, '../')

## Configuración Login
URL_LOGIN ='http://127.0.0.1:5000/login'
URL_OBTENER_CANAL ='http://127.0.0.1:5000/api/canales'
USUARIO_AUTORIZADOR = { "usuario": "ccp", "contrasena": "usuario1"}

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
        respLogin = json.loads(login.content.decode('utf-8'))
        token = respLogin['data']

        # Obtiene canal marketing para escuchar peticiones
        respCanal = requests.get(URL_OBTENER_CANAL, headers = {"Authorization": 'Bearer ' + token})
        canales_marketing = json.loads(respCanal.content.decode('utf-8'))['data']
        canal_autorizado = canales_marketing[0]

        print('Escuchando mensajes del canal', canal_autorizado)
        sub.subscribe(canal_autorizado)
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
                redis_db.publish(CANAL_OFERTAS, json.dumps(oferta))
                
            time.sleep(0.01)
