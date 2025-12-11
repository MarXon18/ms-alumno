import logging
import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# CORRECCIÓN: Importamos la función 'factory' directamente, no el diccionario 'config'
from app.config import factory 

# 1. Definimos las extensiones globalmente
db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    """
    Application Factory Pattern
    """
    app = Flask(__name__)
    
    # Configuración del entorno
    app_context = os.getenv('FLASK_CONTEXT', 'development')
    
    # CORRECCIÓN: Usamos la función importada directamente
    config_obj = factory(app_context)
    app.config.from_object(config_obj)
    
    # 2. Inicializamos las extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 3. REGISTRO DE BLUEPRINTS
    # Importamos dentro de la función para evitar dependencias circulares
    from app.routes import alumno_bp 
    app.register_blueprint(alumno_bp)

    @app.shell_context_processor    
    def ctx():
        return {"app": app, "db": db}
    
    return app

# Instancia global para Gunicorn
app = create_app()
