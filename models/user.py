import uuid

from pydantic import BaseModel, Field, Required


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Required
    email: str = Required
    password: str = Required
    role: str = Required
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "username": "admin",
                "email": "tuan@email.com",
                "password": "$2b$12$6UUqjEoXU51GGgj6OH.oOuqupcOspjpCKAVcjcdOyYgqN7xv9X1Aa",
                "role": "admin",
                "is_active": True
            }
        }
