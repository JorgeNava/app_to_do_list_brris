from flask import request, redirect, url_for
from flask import Blueprint, redirect, request, jsonify, url_for, render_template
from database.database_manager import database_manager
from bson import ObjectId
import os
from bson import ObjectId
from app.logic.task_logic import add_task_logic
from app.logic.task_logic import update_task


task_bp = Blueprint('task', __name__)

# Accede a las variables de entorno
DB_URI = os.getenv('MONGO_URI')

@task_bp.route('/tasks', methods=['GET'])
def list_tasks():
    # Obtener la colección de tareas directamente desde la instancia de database_manager
    tasks_collection = database_manager.get_db()['tasks']
    tasks = list(tasks_collection.find())  # Obtener todas las tareas y convertir el cursor a una lista
    return jsonify(tasks)

@task_bp.route('/add-task', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    task_priority = request.form.get('task_priority')

    # Llamar a la lógica para agregar la tarea
    add_task_logic(task_name, task_priority, database_manager)

    return redirect(url_for('home.home'))  # Redirige de vuelta a la página de inicio


@task_bp.route('/edit-task/<task_id>', methods=['POST'])
def edit_task(task_id):
    new_name = request.form.get('new_name')
    new_priority = request.form.get('new_priority')

    update_task(task_id, new_name, new_priority)
    return redirect(url_for('home.home'))


@task_bp.route('/tasks-delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    if request.form.get('_method') == 'DELETE':
        print(f"Request method: {request.method}")
        print(f"Task ID received: {task_id}")

        try:
            # Convertir task_id a ObjectId
            query = {'_id': ObjectId(task_id)}

            deleted_count = database_manager.delete('tasks', query)

            if deleted_count > 0:
                print(f"Tarea con ID {task_id} eliminada correctamente.")
                return redirect(url_for('home.home'))
            else:
                print(f"No se encontró una tarea con ID {task_id}.")
                return redirect(url_for('home.home'))
        except Exception as e:
            print(f"Error al eliminar la tarea: {e}")
            return redirect(url_for('home.home'))
    else:
        return redirect(url_for('home.home'))
