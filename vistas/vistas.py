from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from flask_restful import Resource
import hashlib
from modelos import db, Usuario
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
            additional_claims = {
                "usuario": usuario.usuario,
                "token": otp
            }
            token_de_acceso = create_access_token(identity=usuario.id, additional_claims=additional_claims)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id}
