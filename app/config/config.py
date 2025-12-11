import os
from dotenv import load_dotenv
from pathlib import Path

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Configuración base
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'

class ProductionConfig(Config):
    # --- AQUÍ LA MAGIA PARA TU DOCKER-COMPOSE ---
    # Leemos las variables desglosadas (HOST, USER, PASS, NAME)
    DB_USER = os.environ.get('USER_DB', 'sysacad')
    DB_PASS = os.environ.get('PASSWORD_DB', 'password')
    DB_HOST = os.environ.get('HOST_DB', 'localhost')
    DB_NAME = os.environ.get('NAME_DB', 'sysacad_db')
    
    # Construimos la URI completa para SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# El diccionario debe ir AL FINAL, cuando todas las clases ya existen
config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def factory(app_context: str) -> Config:
    """
    Retorna la clase de configuración según el entorno.
    Si el entorno no existe en el diccionario, usa 'default'.
    """
    return config.get(app_context, config['default'])
