from flask import Blueprint, redirect, request, url_for, render_template, flash
from database.database_manager import database_manager
from werkzeug.security import generate_password_hash
import os

from app.logic.users_logic import add_user_logic

user_bp = Blueprint('user',__name__)

# Accede a las variables de entorno
DB_URI = os.getenv('MONGO_URI')

@user_bp.route('/register', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email_user = request.form.get('email')
        password_user = request.form.get('password')

        # Llamar a la lógica para agregar el usuario
        add_user_logic(email_user, password_user)

        # Redirige a la página de inicio de sesión después del registro
        return redirect(url_for('user.get_user'))

    return render_template('register.html')

@user_bp.route('/', methods=['GET', 'POST'])
def get_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Buscar al usuario por su email y contraseña
        user = database_manager.select(
            db_name=None,  # Puedes omitir esto si estás usando la base de datos predeterminada
            collection_name='users',  # Nombre de la colección
            query={'email': email, 'password': password}  # Consulta para encontrar al usuario
        )
        
        # Convertir el cursor de MongoDB a una lista y verificar si hay resultados
        user_list = list(user)
        if user_list:
            # Si encuentra un usuario con ese email y contraseña
            flash("Has iniciado sesión exitosamente.", 'success')
            return redirect(url_for('home.home'))  # Asegúrate de que 'home.home' sea un endpoint válido
        else:
            # Si no encuentra coincidencia
            flash("Email o contraseña incorrectos.", 'error')
    
    return render_template('login.html')
