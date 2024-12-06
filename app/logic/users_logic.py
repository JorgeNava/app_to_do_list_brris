from database.database_manager import database_manager
from werkzeug.security import generate_password_hash, check_password_hash


def add_user_logic(email_user, password_user):
    """
    Función para agregar un usuario a la base de datos con contraseña hasheada.
    """
    # Generar el hash de la contraseña
    hashed_password = generate_password_hash(password_user)

    # Estructura del usuario
    user_data = {
        'email': email_user,
        'password': hashed_password  # Guardar la contraseña hasheada
    }

    # Nombre de la colección
    collection_name = 'users'

    # Insertar el usuario en la base de datos
    inserted_user = database_manager.insert(
        db_name=None,
        collection_name=collection_name,
        data=user_data
    )

    # Imprimir para verificar la inserción
    print(f"Inserted user: {inserted_user}")
    return inserted_user


def verify_user_logic(email_user, password_user):
    """
    Verifica las credenciales del usuario.
    """
    # Buscar al usuario en la base de datos por su email
    user = database_manager.select(
        db_name=None,
        collection_name='users',
        query={'email': email_user}
    )

    # Convertir el cursor en una lista
    user_list = list(user)

    if not user_list:
        # Usuario no encontrado
        return False

    # Obtener el hash de la contraseña almacenada
    stored_password_hash = user_list[0]['password']

    # Verificar la contraseña ingresada contra el hash almacenado
    return check_password_hash(stored_password_hash, password_user)
