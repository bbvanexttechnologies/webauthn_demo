# FIDO Register & Login DEMO

Este Proyecto es una DEMO del estándar FIDO2 para autenticación sin contraseñas.
Para la parte del servidor se ha empleado Python con el

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._


### Pre-requisitos 📋

Docker y docker-compose.
Es necesario que el dispositivo cuente con huella dactilar compatible con FIDO o bien que se disponga de una llave física compatible con FIDO.


### Instalación 🔧

Construir las imágenes
```
docker-compose up
```

Acceder al frontal en el navegador
```
localhost:8080
```


## Notas 📦

WebAuthn javascript will work only when used with HTTPS or on the localhost hostname (in this case HTTPS is not required).


## Construido con 🛠️


* [py_webauthn](https://github.com/duo-labs/py_webauthn) - FIDO Module for Python
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Python Server
* [VueJS](https://vuejs.org/) - Framework Front
* [Vuetify](https://vuetifyjs.com/en/) - VUE UI Library




---
⌨️ con ❤️ por Cybersecurity Lab




