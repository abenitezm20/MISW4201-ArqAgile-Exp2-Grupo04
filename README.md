# MISW4201-ArqAgile-Exp2-Grupo04

> para configurar el servicio autorizador de canales porfavor revisar el readme.md de la carpeta AutorizadorMensajes

Se debe tener el servidor de redis corriendo

# orden de levantamiento de servicios

1. levantar componente autorizador
```
cd AutorizadorMensajes
flask run -p 5001
```

2. levantar componentes marketing
```
cd marketing
flask run -p 5002
```
```
cd marketing_2
flask run -p 5003
```

3. levantar componente principal
```
flask run -p 5000
```

# Uso del sistema

1. Realizar login a la url: http://127.0.0.1:5000/login
```javascript
{
    "usuario": "admin",
    "contrasena": "admin"
}
```
para ejemplos prácticos se retorna el OTP en esta petición, en la realidad se envia es por correo

2. Validar el otp recibido en la url: http://127.0.0.1:5000/validar
```javascript
{
    "usuario": "admin",
    "otp": 563113
}
```
Se obtiene como respuesta el token
```javascript
{
    "mensaje": "Inicio de sesión exitoso",
    "token": "eyJhbGc......",
    "id": 1
}
```
3. realizar una oferta en la url: http://127.0.0.1:5000/crearOferta
```javascript
{
    "oferta": "oferta2",
    "producto": "producto2"
}
```
Como respuesta se obtienen los canales a los que se pueden publicar
```javascript
{
    "respuesta_canales": [
        "hxfrcmru"
    ]
}
```