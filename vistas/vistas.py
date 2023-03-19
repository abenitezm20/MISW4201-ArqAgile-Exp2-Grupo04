import logging
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity
from flask_restful import Resource
import hashlib
from modelos import db, Usuario, OTP
from Logica.Logica import Logica
import requests
import json
from handler import Handler



login_autorizador='http://127.0.0.1:5001/login'
canales_autorizador='http://127.0.0.1:5001/api/canales'

logging.basicConfig(level=logging.INFO, filename='audit.log', encoding='utf-8', format='%(asctime)s %(message)s')

class VistaLogIn(Resource):
    
    def post(self):
        contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == contrasena_encriptada).first()
        db.session.commit()
        if usuario is None:
            logging.error(f'El usuario no existe')
            return "El usuario no existe", 404
        else:
            otp = Logica.generarCodigoOTP()
            nuevo_otp = OTP(otp=otp, id_usuario=usuario.id, usuario=usuario.usuario)
            db.session.add(nuevo_otp)
            db.session.commit()
            logging.info('Se genero codigo OTP para usuario: '+usuario.usuario)
            return otp
        

class VistaValidarOTP(Resource):
    
    def post(self):
        otp_almacenado = OTP.query.filter(OTP.otp == request.json["otp"],
                                          OTP.usuario == request.json["usuario"]
                                          ).first()
        db.session.commit()
        if otp_almacenado is None:
            logging.error(f'Acceso no autorizado')
            return "El OTP no existe", 404
        else:
            logging.info('el usuario  '+otp_almacenado.usuario+' se autentico con exito')
            additional_claims = {
                "usuario": otp_almacenado.usuario,
            }
            token_de_acceso = create_access_token(identity=otp_almacenado.id_usuario, additional_claims=additional_claims)
            db.session.delete(otp_almacenado)
            db.session.commit()
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": otp_almacenado.id_usuario}


class VistaCrearOferta(Resource):
    
    @jwt_required()
    def post(self):
        
        oferta={"data":{'product':request.json["producto"],"oferta" :request.json["oferta"]}}

        #Validar usuario en el autorizador
        id_usuario = get_jwt_identity()
        json_usuario={"usuario": "ccp", "contrasena": "usuario1"}
        registro_autorizador = requests.post(login_autorizador, json = json_usuario )
        respuesta_autorizador = json.loads(registro_autorizador.content.decode('utf-8'))
        token_autorizador = respuesta_autorizador['data']
        
        #Solicitar canales al autorizador
        respCanal = requests.get(canales_autorizador, headers = {"Authorization": 'Bearer ' + token_autorizador})
        respuesta_canales = json.loads(respCanal.content.decode('utf-8'))['data']
        for canal in respuesta_canales:
            Handler.publicar(oferta=json.dumps(oferta).encode('utf-8'),canal=canal, id_usuario=str(id_usuario))

        return {"respuesta_canales":respuesta_canales}
        


