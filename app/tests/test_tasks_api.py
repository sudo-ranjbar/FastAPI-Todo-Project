def test_tasks_response_401(anonymous_client):
    response = anonymous_client.get("api/v1/tasks")
    assert response.status_code == 401

def test_tasks_response_200(authenticated_client):
    response = authenticated_client.get("api/v1/tasks")
    assert response.status_code == 200

def test_random_task_200(authenticated_client, random_task):
    """random_task is not a function inside your test. It's already the object returned by the fixture."""
    task_obj = random_task
    response = authenticated_client.get(f"api/v1/tasks/{task_obj.id}")
    assert response.status_code == 200