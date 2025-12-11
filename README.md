# ms-alumno

## Descripción
El Microservisio Alumno es una API REST de gestión académica construida con **Flask**, **SQLAlchemy**, **Marshmallow** y **PostgreSQL**.

## Equipo de desarrollo
- Marcos Aranda
- Luanna Guajardo
- Axel Sanchez
- Lucas Becerra
- Joaquín Moliterno
  
## SysAcad
- https://github.com/MarXon18/SysAcad
## Requerimientos
- Python 3.10+
- PostgreSQL 13+
- `pip` y `virtualenv`
- *(Opcional)* Docker + Docker Compose

> En `requirements.txt` usar **un solo** driver de Postgres (psycopg2 **o** psycopg/psycopg[binary]).

## Estructura del proyecto
carpeta/app - es la carpeta contenedora de toda la logica del proyecto es donde se crea la base del proyecto y es la base donde se trabajara.

carpeta/test - es la carpeta dedicada a los distintos test que se realizaran al proyecto para corroborar la conexion de estos con la base de datos con la cual se trabajara.

carpeta/docker- es la carpeta que va servir para mantener ordenado el proyecto, guardar configuraciones y para facilitar el entorno de desarrollo de la aplicacion.

## Instalación
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows (PowerShell)
# .\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

Configuración (.env)

Copiar env-example → .env y completar credenciales:
## --- Configuración de Redis ---
## Generalmente localhost o 127.0.0.1 para desarrollo local
#REDIS_HOST=127.0.0.1

## El puerto por defecto de Redis es 6379
#REDIS_PORT=6379

## Si no tienes contraseña en local, puedes dejarlo vacío o poner una cadena
#REDIS_PASSWORD=1234

## --- Configuración de Base de Datos ---
## Host de la DB (localhost, IP o URL de AWS RDS/DigitalOcean)
#HOST_DB=localhost

## Usuario principal (ej. root, postgres, admin)
#USER_DB=Alumno

## Contraseña de acceso a la base de datos
#PASSWORD_DB=12345678

## El nombre exacto de la base de datos a la que te conectarás
#NAME_DB=ms_alumno

#SQLALCHEMY_TRACK_MODIFICATIONS=False
#SQLALCHEMY_RECORD_QUERIES=True
#FLASK_CONTEXT=development
#TEST_DATABASE_URI=postgresql+psycopg2://nombre:12345678@localhost:5432/TEST_SYSACAD
#DEV_DATABASE_URI=postgresql+psycopg2://nombre:12345678@localhost:5432/DEV_SYSACAD
#PROD_DATABASE_URI=postgresql://nombre:12345678@localhost:5432/SYSACAD


Migraciones
flask db init
flask db migrate -m "init"
flask db upgrade

Ejecución
export FLASK_CONTEXT=development   # Windows: set FLASK_CONTEXT=development
python app.py
# http://localhost:5000
# Healthcheck: GET /api/v1/  -> "OK"

Endpoints mínimos
GET /api/v1/ (healthcheck)
GET /api/v1/universidad
GET /api/v1/universidad/<id>
POST /api/v1/universidad
DELETE /api/v1/universidad/<id>

Pruebas
Opción A
export FLASK_CONTEXT=testing   # Windows: set FLASK_CONTEXT=testing
python -m unittest discover -s test -p "test_*.py" -v
Opción B
pytest -q
Todos los test deben pasar y la aplicación debe ejecutarse sin errores

Docker
docker build -t flask-sysacad:v1.0.0 .
# si el compose requiere una red externa:
docker network create mired
docker compose -f docker/docker-compose.yml up -d
