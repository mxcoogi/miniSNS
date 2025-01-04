from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from user.application.user_service import UserService
from typing import Annotated
from dependency_injector.wiring import inject, Provide
from containers import Container
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    name : str
    email : str
    password : str

@router.post("", status_code=201)
@inject
def create_user(user:CreateUserBody, user_service : UserService = Depends(Provide[Container.user_service])):
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password = user.password
    )
    return created_user

class UpdateUserBody(BaseModel):
    name : str | None = None
    password : str | None = None

@router.put("/{user_id}")
@inject
def update_user(
    user_id : str,
    user : UpdateUserBody,
    user_service : UserService = Depends(Provide[Container.user_service])
):
    user = user_service.update_user(user_id, user.name, user.password)

    return user



@router.get("")
@inject
def get_users(page : int = 1,
              item_per_page : int = 10,
              user_service : UserService = Depends(Provide[Container.user_service])):
    
    total_count, users = user_service.get_users(page, item_per_page)

    return {
        "total_count":total_count,
        "page" : page,
        "users" : users
    }

@router.post("/login")
@inject
def login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service : UserService = Depends(Provide[Container.user_service])
):
    access_token = user_service.login(
        email = form_data.username,
        password = form_data.password
    )

    return {"access_token" : access_token, "token_type" : "bearer"}