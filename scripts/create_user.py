# scripts/create_user.py
from app.db.deps import get_db
from app.services.user_service import UserService

def main():
    service = UserService()

    for db in get_db():
        user = service.register(
            db,
            email="test@example.com",
            username="testuser",
        )
        print("created user:", user.user_id)

if __name__ == "__main__":
    main()
