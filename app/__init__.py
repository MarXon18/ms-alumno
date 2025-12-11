import logging
import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config

# 1. Definimos las extensiones globalmente (pero sin inicializar)
db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    """
    Application Factory Pattern
    """
    app = Flask(__name__)
    
    # Configuración del entorno
    app_context = os.getenv('FLASK_CONTEXT', 'development')
    config_obj = config.factory(app_context)
    app.config.from_object(config_obj)
    
    # 2. Inicializamos las extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 3. REGISTRO DE BLUEPRINTS (El cambio importante)
    # Importamos el Blueprint que creamos en routes.py (o resources.py)
    # Nota: Asegúrate de que 'app.routes' sea el nombre correcto de tu archivo de rutas.
    from app.routes import alumno_bp 
    app.register_blueprint(alumno_bp)

    @app.shell_context_processor    
    def ctx():
        return {"app": app, "db": db} # Agregué 'db' por si quieres usarlo en la shell
    
    return app

# Esta línea permite correrlo con "flask run" o Gunicorn buscando "app:app"
app = create_app()
