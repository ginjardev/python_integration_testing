import pytest
import os
from samples.flask_api.app import app, DB_FILE, init_db
from conftest import set_test_status

@pytest.fixture(autouse=True)
def setup_and_teardown_db(tmp_path):
    # Override the DB_FILE to point to a temporary database file
    test_db_file = tmp_path / "test.db"
    app.config["TESTING"] = True

    # Monkey patch the DB_FILE used in the app
    global DB_FILE
    DB_FILE = str(test_db_file)
    init_db()

    yield  # Run the test

    # Cleanup is handled by tmp_path automatically
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

@pytest.fixture
def client():
    return app.test_client()



def test_add_user(client, set_test_status):
    try:
        # Add a user via POST
        response = client.post("/users", json={"name": "Joe"})
        assert response.status_code == 201
        assert response.get_json()["message"] == "User added"
        set_test_status(status="passed", remark="API builds metadata returned")
    except AssertionError as e:
        set_test_status(status="failed", remark="API sessions metadata not returned")
        raise (e)



def test_get_user(client, set_test_status):
    try:
        # Retrieve users via GET
        response = client.get("/users")
        assert response.status_code == 200
        data = response.get_json()
    
        assert len(data) == 1
        assert data[0]["name"] == "Joe"
        assert "id" in data[0]
        set_test_status(status="passed", remark="API builds metadata returned")
    except AssertionError as e:
        set_test_status(status="failed", remark="API sessions metadata not returned")
        raise (e)

