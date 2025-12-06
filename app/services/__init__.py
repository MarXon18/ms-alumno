import logging
from flask import Flask
import os
from flask_migrate import Migrate
from app.config import config
from app.resources import init_routes
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    app = Flask(__name__)
    app_context = os.getenv('FLASK_CONTEXT', 'development')
    config_obj = config.factory(app_context)
    app.config.from_object(config_obj)
    db.init_app(app)
    migrate.init_app(app,db)
    init_routes(app)

    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app

# Se crea la instancia de la aplicación aquí para que Gunicorn pueda encontrarla como 'app.app'.
app = create_app()