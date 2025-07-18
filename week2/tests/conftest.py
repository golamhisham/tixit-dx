import os
import pytest
from app.database import Base, engine

# Use file-based SQLite for tests
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

@pytest.fixture(autouse=True, scope="session")
def clean_db():
    db_path = "test.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    if os.path.exists(db_path):
        os.remove(db_path) 