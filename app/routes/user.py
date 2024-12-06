from flask import Blueprint, redirect, url_for, session, request, flash, render_template
from database.database_manager import database_manager
from app.logic.users_logic import add_user_logic, verify_user_logic  # Asegúrate de tener esta función
import os

user_bp = Blueprint('user', __name__)

# Obtén la instancia de OAuth desde la app principal
from app import oauth

@user_bp.route('/register', methods=['GET', 'POST'])
def add_user():
    """
    Ruta para registrar un nuevo usuario.
    """
    if request.method == 'POST':
        email_user = request.form.get('email')
        password_user = request.form.get('password')

        # Llamar a la lógica para agregar el usuario
        add_user_logic(email_user, password_user)

        # Redirige a la página de inicio de sesión después del registro
        flash("Registro exitoso. Por favor inicia sesión.", 'success')
        return redirect(url_for('user.get_user'))

    return render_template('register.html')

@user_bp.route('/', methods=['GET', 'POST'])
def get_user():
    """
    Ruta para manejar el inicio de sesión local.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar las credenciales del usuario
        if verify_user_logic(email, password):
            flash("Has iniciado sesión exitosamente.", 'success')
            session['user_email'] = email  # Guarda el email del usuario en la sesión
            return redirect(url_for('home.home'))
        else:
            flash("Email o contraseña incorrectos.", 'error')

    return render_template('login.html')

# Nuevas rutas para integración de Auth0
@user_bp.route('/login')
def login():
    """
    Redirige al usuario a Auth0 para autenticación.
    """
    return oauth.auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_CALLBACK_URL'))

@user_bp.route('/auth/callback')
def auth_callback():
    """
    Maneja el callback después de la autenticación en Auth0.
    """
    token = oauth.auth0.authorize_access_token()
    user_info = oauth.auth0.parse_id_token(token)

    if not user_info:
        flash('Error al iniciar sesión.', 'error')
        return redirect(url_for('user.get_user'))

    # Verificar si el usuario ya existe en la base de datos
    user = database_manager.select(
        db_name=None,
        collection_name='users',
        query={'email': user_info['email']}
    )
    user_list = list(user)

    if not user_list:
        # Registrar al usuario si no existe
        add_user_logic(user_info['email'], None)

    # Guardar información del usuario en la sesión
    session['user'] = user_info
    flash('Inicio de sesión exitoso.', 'success')
    return redirect(url_for('home.home'))

@user_bp.route('/logout')
def logout():
    """
    Cierra la sesión del usuario y redirige a la página principal.
    """
    session.pop('user', None)
    session.pop('user_email', None)  # Elimina también la sesión del login local
    flash('Has cerrado sesión.', 'success')
    return redirect(f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?client_id={os.getenv("AUTH0_CLIENT_ID")}&returnTo={url_for("user.get_user", _external=True)}')
