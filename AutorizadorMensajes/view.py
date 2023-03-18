from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from helper import encrypt, crear_o_retorna_canal, retornar_canales, revocar_usuario
from modelos import Usuario, Rol
from flask_jwt_extended import create_access_token

class Login(Resource):

    def post(self):
        usuario = request.json.get('usuario', None)
        contrasena = request.json.get('contrasena', None)

        if usuario is None or contrasena is None:
            return {'error': 'no se permiten campos vacios'}

        usuario = Usuario.query.filter(Usuario.usuario==usuario, Usuario.contrasena==encrypt(contrasena)).first()
        if usuario is None:
            return {'error': 'usuario no encontrado'}
        
        additional_claims = {
            'rol': usuario.rol
        }
        token = create_access_token(identity=usuario.id, additional_claims=additional_claims)
        
        return {'data': token}
    
class Canales(Resource):

    @jwt_required()
    def get(self):
        rol_usuario = get_jwt()['rol']
        user_id = get_jwt_identity()
        canal = None
        if rol_usuario == Rol.cliente:
            try:
                canal = crear_o_retorna_canal(user_id)
            except Exception as e:
                return f'error: {e}', 400
        else:
            canal = retornar_canales()
        return {"data": canal}

class Revocar(Resource):

    @jwt_required()
    def post(self):
        rol_usuario = get_jwt()['rol']
        usuario_id = request.json.get('usuario_id', None)
        if rol_usuario != Rol.usuario:
            return "no tiene permisos de revocar canales", 400
        
        revocar_usuario(usuario_id)
        return "OK"
