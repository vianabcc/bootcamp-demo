from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas, utils, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Bootcamp API",
    description="Example API",
    version="0.1",
    openapi_tags=utils.openapi_tags
)

@app.get("/users/", tags=utils.USER_TAGS, response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(utils.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", tags=utils.USER_TAGS, response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(utils.get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

@app.post("/users/", tags=utils.USER_TAGS, response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.AddUser, db: Session = Depends(utils.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@app.put("/users/{user_id}", tags=utils.USER_TAGS, response_model=schemas.User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, data: schemas.UpdateUser, db: Session = Depends(utils.get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_by_email = crud.get_user_by_email(db=db, email=data.email)
    if user_by_email and user_by_email.id != user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Another user already registered the email '{data.email}'")

    return crud.update_user(db=db, data=data, user_id=user_id)

@app.delete("/users/{user_id}", tags=utils.USER_TAGS, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(utils.get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return crud.delete_user(db=db, user_id=user_id)

@app.patch("/users/{user_id}", tags=utils.USER_TAGS, response_model=schemas.User, status_code=status.HTTP_200_OK)
def toggle_user_is_active(user_id: int, db: Session = Depends(utils.get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return crud.toggle_user_is_active(db=db, user_id=user_id)