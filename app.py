import hashlib
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db, Usuario
from vistas.vistas import VistaLogIn, VistaValidarOTP, VistaCrearOferta, VistaLogInUsuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

#Se crea un usuario inicial
usuario = Usuario.query.filter(Usuario.usuario == 'admin').first()
usuario2 = Usuario.query.filter(Usuario.usuario == 'ccp').first()
if usuario is None:
    contrasena_encriptada = hashlib.md5("admin".encode('utf-8')).hexdigest()
    nuevo_usuario = Usuario(usuario='admin', contrasena=contrasena_encriptada)
    db.session.add(nuevo_usuario)
    db.session.commit()

if usuario2 is None:
    nuevo_usuario2 = Usuario(usuario='ccp', contrasena='usuario1')
    db.session.add(nuevo_usuario2)
    db.session.commit()


api = Api(app)
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaValidarOTP, '/validar')
api.add_resource(VistaCrearOferta, '/crearOferta')
api.add_resource(VistaLogInUsuario, '/loginUsuario')


jwt = JWTManager(app)