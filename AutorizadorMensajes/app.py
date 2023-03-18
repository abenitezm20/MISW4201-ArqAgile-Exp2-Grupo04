from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from view import Login, Canales, Revocar
from modelos import db, Usuario, Rol, Habilitado
from helper import encrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autorizador.sqlite'
app.config['JWT_SECRET_KEY'] = 'supersecret'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=10)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)

db.init_app(app)
db.create_all()

with app_context:
    Usuario.query.delete()
    Habilitado.query.delete()
    user1 = Usuario(usuario='ccp', contrasena=encrypt('usuario1'), rol=Rol.usuario)
    user2 = Usuario(usuario='cliente1', contrasena=encrypt('cliente1'), rol=Rol.cliente)
    user3 = Usuario(usuario='cliente2', contrasena=encrypt('cliente2'), rol=Rol.cliente)
    db.session.add_all([user1,user2,user3])
    db.session.commit()
    habilitado1 = Habilitado(usuario_id=user2.id)
    habilitado2 = Habilitado(usuario_id=user3.id)
    db.session.add_all([habilitado1,habilitado2])
    db.session.commit()

api = Api(app)
api.add_resource(Login, "/login")
api.add_resource(Canales, "/api/canales")
api.add_resource(Revocar, "/api/canal/revocar")
