from typing import Any

from fastapi import Depends, status
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class GetMyAccountResponse(AppModel):
    id: Any = Field(alias="_id")
    email: str
    phone: str
    name: str
    city: str


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