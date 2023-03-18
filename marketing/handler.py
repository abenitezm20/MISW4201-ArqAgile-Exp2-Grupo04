import time
import sys
import json
import redis

from faker import Faker

sys.path.insert(0, '../')

CANAL_MARKETING = 'marketing_receptor';
CANAL_OFERTAS = 'marketing_ofertas';
REDIS_CONNECTION = redis.Redis(host='localhost', port=6379, db=0)

redis_db = REDIS_CONNECTION
sub = redis_db.pubsub()
sub.subscribe(CANAL_MARKETING)

class Handler():
    @staticmethod
    def escuchar():
        print('Escuchando mensajes del canal', CANAL_MARKETING)
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
