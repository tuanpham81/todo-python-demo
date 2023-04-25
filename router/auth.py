from datetime import timedelta, datetime
from typing import Optional

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status

from database import collection_user
from models.user import User


app = FastAPI()
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "Copybox2023"
ALGORITHM = "HS256"


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = create_access_token(user["username"], user["_id"], timedelta(minutes=20))
    return {"access_token": token, "token_type": "Bearer"}


def authenticate(username: str, password: str):
    user = collection_user.find_one({"username": username})
    if user is None:
        return False
    if not bcrypt_context.verify(password, user['password']):
        return False
    return user


def create_access_token(username: str, user_id: str,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post('/create-user')
async def create_user(create_user_request: User):
    create_user_request.password = bcrypt_context.hash(create_user_request.password)
    create_user_request = jsonable_encoder(create_user_request)
    new_user = collection_user.insert_one(create_user_request)
    created_user = collection_user.find_one(
        {"_id": new_user.inserted_id})
    return created_user
