from application import app, db

app.config["TESTING"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
client = app.test_client()


with app.app_context():
    db.create_all()


def test_add_task():
    response = client.post('/tasks', json={"name" : "Test Task", "description":"Testing"})
    assert response.status_code == 200


def test_task_list():
    response = client.get('/tasks')
    assert response.status_code == 200

    assert len(response.json["tasks"]) > 0

def test_delete_task():
    response = client.delete('/tasks/1')
    assert response.status_code == 200
