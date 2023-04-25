import uuid
from typing import Optional

from pydantic import BaseModel, Field, Required


class Todo(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    description: str = Required
    # description: str = Field(...)
    is_done: bool = False
    user_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "description": "coding",
                "is_done": False,
                "user_id": "123"
            }
        }


class TodoUpdate(BaseModel):
    description: Optional[str]
    is_done: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "description": "sleep",
                "is_done": True
            }
        }
