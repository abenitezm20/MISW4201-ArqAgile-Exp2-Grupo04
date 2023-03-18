import logging
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from flask_restful import Resource
import hashlib
from modelos import db, Usuario, OTP
from Logica.Logica import Logica

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
