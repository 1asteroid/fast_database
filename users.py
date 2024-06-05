from fastapi import APIRouter
from database import Session, ENGINE
from pydantic import BaseModel
from typing import Optional
from models import Users
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from werkzeug import security


session = Session(bind=ENGINE)

auth_router = APIRouter(prefix="/auth")


class RegisterModel(BaseModel):
    username: str
    email: str
    password: str
    reset_password: str


class LoginModel(BaseModel):
    username: str
    password: str


@auth_router.get("/")
async def auth():
    return {
        "message": "This is auth page"
    }


@auth_router.post("/register")
async def register(user: RegisterModel):

    if user.reset_password != user.password:
        return {
            "message": "password and reset_password are not like"
        }

    username = session.query(Users).filter(Users.username == user.username).first()
    if username:
        message = f"{user.username} username already exists"
        return {
            "message": message
        }

    email = session.query(Users).filter(Users.email == user.email).first()
    if email:
        message = f"This {user.email} is in use"
        return {
            "message": message
        }

    new_user = Users(
        username=user.username,
        password=security.generate_password_hash(user.password),
        email=user.email
    )
    session.add(new_user)
    session.commit()

    return HTTPException(status_code=status.HTTP_201_CREATED)


@auth_router.post("/login")
async def login(user: LoginModel):

    check_user = session.query(Users).filter(Users.username == user.username).first()

    if check_user:
        password = check_user.password

        if security.check_password_hash(password, user.password):
            return HTTPException(status_code=status.HTTP_200_OK, detail={"username": user.username,
                                                                         "message": "User found"})

        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"username": user.username,
                                                                                "message": "Password incorrect"})

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"username": user.username,
                                                                        "message": "No user with this username"})






