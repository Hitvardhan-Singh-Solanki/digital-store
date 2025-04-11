from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str

    class Config:
        orm_mode = True


class UserDeleteRequest(BaseModel):
    password: str
