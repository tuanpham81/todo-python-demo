from fastapi import HTTPException, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from starlette import status

from models.todo import Todo, TodoUpdate
from router.auth import get_current_user

router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)

cluster = MongoClient("mongodb+srv://tuan816:Copybox2023@cluster0.pzaped9.mongodb.net/?retryWrites=true&w=majority")
db = cluster["todo-demo"]
# db = cluster.get_database("todo-demo")
collection_todo = db["todo"]
# collection_todo = db.get_collection("todo")


@router.get("/list")
async def get_all_todo(user: dict = Depends(get_current_user)):
    todo_dict = collection_todo.find({"user_id": user["id"]})
    todo_list = [Todo(**todo) for todo in todo_dict]
    return todo_list


@router.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def add_new_todo(create_todo_request: Todo, user: dict = Depends(get_current_user)):
    create_todo_request.user_id = user["id"]
    create_todo_request = jsonable_encoder(create_todo_request)
    new_todo = collection_todo.insert_one(create_todo_request)
    created_todo = collection_todo.find_one(
        {"_id": new_todo.inserted_id})
    return created_todo


@router.put("/update-todo", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(update_request: TodoUpdate, todo_id: str, user: dict = Depends(get_current_user)):
    todo_dict = collection_todo.find_one({"_id": todo_id, "user_id": user["id"]})
    if not todo_dict:
        raise HTTPException(status_code=404, detail="Todo not found")
    collection_todo.update_one(
        {"_id": todo_id},
        {"$set": {
            "description": update_request.description,
            "is_done": update_request.is_done
        }}
    )


@router.delete("/delete-todo", status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: str, user: dict = Depends(get_current_user)):
    delete_result = collection_todo.delete_one({"_id": todo_id, "user_id": user["id"]})
    if delete_result.deleted_count != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {todo_id} not found")
