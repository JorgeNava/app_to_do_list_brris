import pytest
from app import create_app
from database.database_manager import DatabaseManager
import mongomock

@pytest.fixture
def test_client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://mock"
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db():
    db_manager = DatabaseManager()
    db_manager.client = mongomock.MongoClient()
    db_manager.default_db_name = "test_db"
    return db_manager
