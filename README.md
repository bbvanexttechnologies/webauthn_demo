# FIDO Register & Login DEMO

This project is a FIDO2 DEMO that can be used for register and authentication purposes under the FIDO2 paswordless standard.
The FIDO server has been built using Python with an specific opensource module which includes all the functions to work with the standard. This module can be installed using pip.
The fronted has been build using VueJS in conjuction with vuetify.

Furthermore, the whole project has been dockerized and it can be built using docker-compose.

## Init 🚀

This instructions will let you obtain a local copy of the project for development and trial.


### Pre-requirements 📋

It's necessary to have both Docker and docker-compose installed and running on the host machine.
In order to completely try the application it's necessary to have a FIDO device, it can be an external device such as a Yubikey or an embeded element in the laptop such as a fingerprint device.


### Installation 🔧

Build the images with docker-compose
```
docker-compose up
```

Open the web browser
```
localhost:8080
```


## Notes 📦

WebAuthn javascript will work only when used with HTTPS or on the localhost hostname (in this case HTTPS is not required).


## Built with 🛠️


* [py_webauthn](https://github.com/duo-labs/py_webauthn) - FIDO Module for Python
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Python Server
* [VueJS](https://vuejs.org/) - Framework Front
* [Vuetify](https://vuetifyjs.com/en/) - VUE UI Library




---
⌨️ With ❤️ by Cybersecurity Lab




