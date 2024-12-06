def test_task_priority_handling(client, database):
    # Crear tareas con diferentes prioridades
    database['tasks'].insert_many([
        {'task_name': 'Task 1', 'task_priority': 'Baja'},
        {'task_name': 'Task 2', 'task_priority': 'Alta'},
        {'task_name': 'Task 3', 'task_priority': 'Media'}
    ])
    
    # Verificar el orden de las tareas según la prioridad
    tasks = list(database['tasks'].find().sort('task_priority', 1))  # Ordenar por prioridad
    assert tasks[0]['task_priority'] == 'Alta'
    assert tasks[1]['task_priority'] == 'Media'
    assert tasks[2]['task_priority'] == 'Baja'
