from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import enum

db = SQLAlchemy()

class Rol(str, enum.Enum):
    usuario = "usuario"
    cliente = "cliente"

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(Enum(Rol))

class Canal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    canal = db.Column(db.String(50))
    revocado = db.Column(db.Boolean, default=False)

class Habilitado(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    habilitado = db.Column(db.Boolean, default= True)
