from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base,create_engine,sessionmaker,get_db
from sqlalchemy import StaticPool
import pytest
from app.users.models import UserModel
from app.tasks.models import TaskModel
from app.services.hasher import Hasher
from faker import Faker
from app.services.jwt import create_access_token

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# module
@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# module
@pytest.fixture(scope="module", autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)

# session
@pytest.fixture(scope="session", autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# function
@pytest.fixture(scope="function")
def anonymous_client():
    client = TestClient(app)
    yield client

# function
@pytest.fixture(scope="function")
def authenticated_client(db_session):
    client = TestClient(app)
    user = db_session.query(UserModel).filter_by(email="test_email@gmail.com").one()
    access_token = create_access_token({"user_id": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client

# function
@pytest.fixture(scope="function")
def random_task(db_session):
    user = db_session.query(UserModel).filter_by(email="test_email@gmail.com").one()
    task = db_session.query(TaskModel).filter_by(user_id=user.id).first()
    return task

# ============================================Mock Data===============================================
fake = Faker()

@pytest.fixture(scope="package", autouse=True)
def generate_mock_data(db_session):

    hashed_password = Hasher.hash_password("123456")
    user = UserModel(
        username="test_user", email="test_email@gmail.com", password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task_list = []
    for _ in range(5):
        task_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_complete=fake.boolean(),
            )
        )
    db_session.add_all(task_list)
    db_session.commit()