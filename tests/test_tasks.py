def test_task_workflow(test_client):
    response = test_client.post("/tasks", json={"task": "New Task"})
    assert response.status_code == 201

    response = test_client.get("/tasks")
    tasks = response.json
    assert len(tasks) > 0
    assert tasks[0]["task"] == "New Task"

    task_id = tasks[0]["_id"]
    response = test_client.put(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200

    response = test_client.get("/tasks")
    tasks = response.json
    assert tasks[0]["completed"] is True
