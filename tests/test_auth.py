# auth_test.py

import pytest
from flask import url_for
from werkzeug.security import check_password_hash
from bson import ObjectId

# Test para añadir un usuario
def test_add_user(client, mocker):
    email_user = 'test@example.com'
    password_user = 'password123'

    # Mock de la lógica de añadir usuario
    mock_add_user_logic = mocker.patch('app.logic.auth_logic.add_user_logic')

    # Simular el POST request para registrar el usuario
    response = client.post(url_for('auth.add_user'), data={
        'email': email_user,
        'password': password_user
    })

    # Verificar que la lógica fue llamada con los parámetros correctos
    mock_add_user_logic.assert_called_once_with(email_user, password_user)

    # Verificar redirección a la página de login
    assert response.status_code == 302
    assert response.headers['Location'] == url_for('auth.login', _external=True)

# Test para el proceso de login
def test_user_login(client, mocker):
    email_user = 'test@example.com'
    password_user = 'password123'

    # Simular la búsqueda del usuario en la base de datos
    mock_db_select = mocker.patch('database.database_manager.select')
    mock_db_select.return_value = [{'email': email_user, 'password': 'hashed_password'}]

    # Simular la verificación de contraseña
    mock_check_password = mocker.patch('werkzeug.security.check_password_hash')
    mock_check_password.return_value = True

    # Simular el POST request para login
    response = client.post(url_for('auth.login'), data={
        'email': email_user,
        'password': password_user
    })

    # Verificar que la contraseña fue validada correctamente
    mock_check_password.assert_called_once_with('hashed_password', password_user)

    # Verificar redirección a la página principal
    assert response.status_code == 302
    assert response.headers['Location'] == url_for('home', _external=True)
