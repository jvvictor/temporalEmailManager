from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str


class EmailContent(BaseModel):
    user: User
    message: str
