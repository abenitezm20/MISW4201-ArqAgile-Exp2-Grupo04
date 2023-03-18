import logging
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from flask_restful import Resource
import hashlib
from modelos import db, Usuario, OTP
from Logica.Logica import Logica

class VistaLogIn(Resource):
    
    def post(self):
        contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == contrasena_encriptada).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            otp = Logica.generarCodigoOTP()

            nuevo_otp = OTP(otp=otp, id_usuario=usuario.id, usuario=usuario.usuario)
            db.session.add(nuevo_otp)
            db.session.commit()

            #additional_claims = {
            #    "usuario": usuario.usuario,
            #    "token": otp
            #}
            #token_de_acceso = create_access_token(identity=usuario.id, additional_claims=additional_claims)
            
            #return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id}
            return otp


class VistaValidarOTP(Resource):
    
    def post(self):
        logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
        handler = logging.FileHandler('test.log') # creates handler for the log file
        logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

        logger.info("Los parametros de entrada son: otp: " + str(request.json["otp"]) + "  usuario:" + request.json["usuario"])
        otp_almacenado = OTP.query.filter(OTP.otp == request.json["otp"],
                                          OTP.usuario == request.json["usuario"]
                                          ).first()
        db.session.commit()
        if otp_almacenado is None:
            return "El OTP no existe", 404
        else:
            logger.info("EL OTP ES:" + str(otp_almacenado.otp))
            additional_claims = {
                "usuario": otp_almacenado.usuario,
            }
            token_de_acceso = create_access_token(identity=otp_almacenado.id_usuario, additional_claims=additional_claims)
            db.session.delete(otp_almacenado)
            db.session.commit()
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": otp_almacenado.id_usuario}
