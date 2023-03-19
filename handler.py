# import time
import logging
import json
import redis

logging.basicConfig(level=logging.INFO,filename='registro.log', encoding='utf-8', format='%(asctime)s %(message)s')

REDIS_CONNECTION = redis.Redis(host='localhost', port=6379, db=0)
redis_db = REDIS_CONNECTION
sub = redis_db.pubsub()


class Handler():
    @staticmethod
    def publicar(oferta, canal, id_usuario):
        logging.info('Se envia la creacion de oferta: '+str(oferta) +' id_usuario: '+str(id_usuario)+' canal usado: '+canal)
        # sub.subscribe(canal)
        redis_db.publish(canal, oferta)