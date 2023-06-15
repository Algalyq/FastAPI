from typing import Any
from fastapi import Depends, UploadFile,status
from pydantic import Field
from app.utils import AppModel
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordRequestForm
from ..utils.security import check_password
from .errors import InvalidCredentialsException

class GetMyAccountResponse(AppModel):
    id: Any = Field(alias="_id")
    email: str
    phone: str = ""
    name: str = ""
    city: str = ""
    avatar_url: str = ""


@router.get("/users/me", response_model=GetMyAccountResponse)
def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user = svc.repository.get_user_by_id(jwt_data.user_id)
    return user


class UpdateUserRequest(AppModel):
    phone: str
    name: str
    city: str

@router.patch("/users/me", status_code=status.HTTP_200_OK)
def update_data(
    input: UpdateUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.update_user_data(jwt_data.user_id, input)
    return {"status":status.HTTP_200_OK}


class RegisterUserRequest(AppModel):
    email: str
    password: str


class RegisterUserResponse(AppModel):
    email: str


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse
)
def register_user(
    input: RegisterUserRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    if svc.repository.get_user_by_email(input.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )

    svc.repository.create_user(input.dict())

    return RegisterUserResponse(email=input.email)



class AuthorizeUserResponse(AppModel):
    access_token: str
    token_type: str = "Bearer"


@router.post("/users/tokens", response_model=AuthorizeUserResponse)
def authorize_user(
    input: OAuth2PasswordRequestForm = Depends(),
    svc: Service = Depends(get_service),
) -> AuthorizeUserResponse:
    user = svc.repository.get_user_by_email(input.username)

    if not user:
        raise InvalidCredentialsException

    if not check_password(input.password, user["password"]):
        raise InvalidCredentialsException

    return AuthorizeUserResponse(
        access_token=svc.jwt_svc.create_access_token(user=user),
    )
