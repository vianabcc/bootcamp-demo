from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str

class AddUser(BaseUser):
    password: str

    class Config:
        orm_mode = True

class UpdateUser(BaseUser):
    password: str
    is_active: bool

    class Config:
        orm_mode = True

class User(BaseUser):
    id: int
    is_active: bool

    class Config:
        orm_mode = True