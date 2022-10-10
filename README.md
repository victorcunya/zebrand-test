# API REST Test 🚀 

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

### Requerimientos:

- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [Make](https://formulae.brew.sh/formula/make)

### Pasos:

1. Crear archivo .env en raíz del proyecto
En configuración de correo colocar credenciales e.g.(mailtrap)
```sh
DATABASE_URL=postgresql://local:local@zebrand_db/local
SMTP_SERVER=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_TLS=true
EMAIL_DEFAULT_SENDER=no-reply@zebrand.mx
EMAIL_RECIPIENTS='admin@admin.com'
```
2. Construir imagenes (bd y backend)
```sh
$ make build
```
3. Levantar ambiente local
```sh
$ make up
```
4. Ejecutar migraciones
```sh
$ make migrate
```
5. Para visualizar logs del backend (opcional)
```sh
$ make log
```
6. La [documentación](http://localhost:8000/api/docs) del api.
```sh
http://localhost:8000/api/docs
```
7. Las migraciones traen consigo 2 usuarios por default con 
password *admin*
```sh
1. admin@admin.com  [ADMIN_ROLE]
2. user@admin.com   [USER_ROLE]
```
8. Listar todos los comandos help
```sh
$ make
```
