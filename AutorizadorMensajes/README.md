# Servicio Autenticador de plataforma de mensajes

> servicio que se encarga de autorizar el envio de mensajes entre componentes, el servicio genera y emite canales para
que otros servicios se puedan suscribir, el componente principal (cliente) obtiene una lista de canales para publicar, 
el componente suscriptor (usuario) obtiene un string el cuál es el canal al cuál debe suscribirse.
en el momento se tienen 3 cuentas creadas, 1 del sevicio emisor de mensajes (cliente) 2 cuentas receptoras de mensajes (usuarios)

## levantar el servicio

```
cd AutorizadorMensajes
flask run -p 6000
```