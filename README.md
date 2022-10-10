# API REST Test 🚀 

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

### Requerimientos:

- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [Make](https://formulae.brew.sh/formula/make)

### Pasos:

1. Crear archivo .env en raíz del proyecto
```sh
DATABASE_URL=postgresql://local:local@zebrand_db/local
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
