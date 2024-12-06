from flask import Flask, request
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os

# Inicializa OAuth
oauth = OAuth()

def create_app():
    # Crear instancia de Flask
    app = Flask(__name__)

    # Cargar variables de entorno
    load_dotenv()

    # Configuración existente
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inicializar OAuth con la aplicación
    oauth.init_app(app)

    # Configuración de Auth0
    oauth.register(
        name='auth0',
        client_id=os.getenv('AUTH0_CLIENT_ID'),
        client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
        client_kwargs={
            'scope': 'openid profile email',
        },
        server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    )

    @app.before_request
    def before_request():
        # Permitir sobrescribir métodos HTTP usando el campo _method
        if request.method == 'POST' and '_method' in request.form:
            request.method = request.form['_method'].upper()

    # Importar y registrar blueprints
    with app.app_context():
        from app.routes.home import home_bp
        from app.routes.user import user_bp
        from app.routes.tasks import task_bp
        from app.routes.index import index_bp

        # Registrar blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(task_bp)
        app.register_blueprint(index_bp)

    return app
