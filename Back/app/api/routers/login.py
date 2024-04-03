from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.seller import Seller
from app.schemas.buyer import Buyer
from app.schemas.token import Token
from app.api.deps import CurrentUserDep, UserServiceDep
from app.core.security import create_access_token, authenticate_user

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token")
async def login_access_token(
    user_service: UserServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(
        email=form_data.username, password=form_data.password, user_service=user_service
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return Token(access_token=create_access_token(user.email), token_type="bearer")


@router.post("/test-token")
async def test_token(current_user: CurrentUserDep) -> Buyer | Seller:
    """
    Test access token
    """
    return current_user