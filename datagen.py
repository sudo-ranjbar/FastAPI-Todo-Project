from app.core.database import SessionLocal
from sqlalchemy.orm import session
from app.users.models import UserModel
from app.tasks.models import TaskModel
from app.services.hasher import Hasher
from faker import Faker

fake = Faker()


def seed_users(db):
    hashed_password = Hasher.hash_password("123456")
    user = UserModel(
        username=fake.user_name(), email=fake.email(), password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_tasks(db, user, count=10):
    task_list = []
    for _ in range(count):
        task_list.append(
            TaskModel(
                user_id=user.id,
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                is_complete=fake.boolean(),
            )
        )
    db.add_all(task_list)
    db.commit()


def main():
    db = SessionLocal()

    try:
        user = seed_users(db)
        tasks = seed_tasks(db, user)
    finally:
        db.close()


if __name__ == "__main__":
    main()
