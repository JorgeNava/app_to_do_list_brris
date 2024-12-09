def test_insert(mock_db):
    collection_name = "tasks"
    data = {"task": "Test task", "completed": False}
    result = mock_db.insert("test_db", collection_name, data)
    assert result is not None

def test_select(mock_db):
    collection_name = "tasks"
    data = {"task": "Test task", "completed": False}
    mock_db.insert("test_db", collection_name, data)
    query_result = mock_db.select("test_db", collection_name, {"task": "Test task"})
    assert len(query_result) == 1
    assert query_result[0]["task"] == "Test task"
