import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.app.api.dependencies.common import SessionDep
from src.app.core import settings
from src.app.core.security import create_access_token
from src.app.crud import users as user_crud
from src.app.db.schemas import Token

router = APIRouter(tags=["login"])


@router.post("/access-token")
async def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    project_settings = settings.get_project_settings()
    user = await user_crud.authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = datetime.timedelta(minutes=project_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=create_access_token(str(user.id), access_token_expires))
