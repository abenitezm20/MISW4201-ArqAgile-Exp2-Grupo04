import hashlib
from modelos import db, Canal, Habilitado
import random
import string

def encrypt(text):
    text = text.encode('utf-8')
    return hashlib.md5(text).hexdigest()

def crear_o_retorna_canal(usuario_id):
    usuario_habilitado = Habilitado.query.filter(Habilitado.usuario_id==usuario_id, Habilitado.habilitado==True).first()
    if usuario_habilitado is None:
        raise Exception("usuario no esta habilitado")
    
    canal_existente = Canal.query.filter(Canal.usuario_id==usuario_id, Canal.revocado==False).first()
    if canal_existente:
        return canal_existente.canal

    letras = string.ascii_lowercase
    canal_aleatorio = ''.join(random.choice(letras) for i in range(8))
    nuevo_canal = Canal(usuario_id=usuario_id, canal=canal_aleatorio)
    db.session.add(nuevo_canal)
    db.session.commit()
    return canal_aleatorio

def retornar_canales():
    canales = Canal.query.filter(Canal.revocado==False).all()
    return [canal.canal for canal in canales]

def revocar_usuario(usuario_id):
    usuario_habilitado = Habilitado.query.filter(Habilitado.usuario_id==usuario_id, Habilitado.habilitado==True).first()
    if usuario_habilitado is None:
        raise Exception("usuario no esta habilitado")
    
    usuario_habilitado.habilitado = False
    db.session.add(usuario_habilitado)
    db.session.commit()
    
    canal_existente = Canal.query.filter(Canal.usuario_id==usuario_id, Canal.revocado==False).first()
    if canal_existente:
        canal_existente.revocado = True
        db.session.add(canal_existente)
        db.session.commit()
    
