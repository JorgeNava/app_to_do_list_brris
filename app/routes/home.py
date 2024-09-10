from flask import Blueprint, render_template
from database.database_manager import database_manager

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    tasks_collection = database_manager.get_db()['tasks']
    tasks = list(tasks_collection.find())
    return render_template('home.html', tasks=tasks)