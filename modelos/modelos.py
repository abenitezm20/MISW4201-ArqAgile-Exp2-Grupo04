from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.Integer)
    id_usuario = db.Column(db.Integer)
    usuario = db.Column(db.String(50))
        

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True
    id = fields.String()


class OTPSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = OTP
         include_relationships = True
         load_instance = True
