from sqlalchemy.orm import Session
from . import models, schemas, utils


# List all users (GET)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Get user by id (GET)
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Get user by email (GET)
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Create user (POST)
def create_user(db: Session, user: schemas.AddUser):
    user = models.User(email=user.email, hashed_password=utils.get_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Update user (PUT)
def update_user(db: Session, data: schemas.UpdateUser, user_id: int):
    data_dict = vars(data)
    data_dict.update({"hashed_password": utils.get_hash(data.password)})
    data_dict.pop("password")
    db.query(models.User).filter(models.User.id == user_id).update(data_dict)
    db.commit()
    return get_user(db=db, user_id=user_id)

# Toggle user activity (PATCH)
def toggle_user_is_active(db: Session, user_id: int):
    user = get_user(db=db, user_id=user_id)
    db.query(models.User).filter(models.User.id == user_id).update({"is_active": not user.is_active})
    db.commit()
    db.refresh(user)
    return user

# Delete user (DELETE)
def delete_user(db: Session,  user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {"delete": "success"}


