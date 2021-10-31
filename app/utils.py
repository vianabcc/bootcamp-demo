from app.database import SessionLocal

USERS = "users"
USER_TAGS = [USERS]
openapi_tags = [
     {"name": USERS, "description": "CRUD User endpoints"},
]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_hash(string: str):
    return str(string.encode())

