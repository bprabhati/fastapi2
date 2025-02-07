from pydantic import BaseModel
"""
pydantic models validates data
"""


class UserCreate(BaseModel):
    name: str
    age: int
    email : str
    password: str

    # obj=UserCreate("python", "age", "email", "password")

class UserUpdate(BaseModel):
        name: str
        email: str