

import uuid

from fastapi import APIRouter, HTTPException

from src.app.api.dependencies.common import SessionDep
from src.app.api.dependencies.users import CurrentUser
from src.app.core.settings import get_project_settings
from src.app.crud import users as user_crud
from src.app.db.models.user import UserCreate, UserPublic, UsersPublic

router = APIRouter(tags=["users"])

project_settings = get_project_settings()


@router.post("/", response_model=UserPublic)
async def register_user(
    session: SessionDep,
    user_in: UserCreate,
) -> UserPublic:
    """
    Create new user
    """
    if user := await user_crud.get_user(session, email=user_in.email):
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists. Please login.",
        )
    user = await user_crud.create_user(session, user_create=user_in)
    return UserPublic.model_validate(user)


@router.post("/create_super_user", response_model=UserPublic)
async def create_super_user(
    session: SessionDep,
) -> UserPublic:
    """
    Create superuser
    """
    print(project_settings.SUPER_USER_PASSWORD)
    user_in = UserCreate(
        email=project_settings.SUPER_USER_EMAIL,
        password=project_settings.SUPER_USER_PASSWORD,
        name="Super",
        surname="User",
        date_of_birth="2000-01-01",
        is_admin=True,
    )
    if await user_crud.get_user(session, email=user_in.email):
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists. Please login.",
        )
    user = await user_crud.create_user(session, user_create=user_in)
    return UserPublic.model_validate(user)


@router.get("/", response_model=UsersPublic)
async def read_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> UsersPublic:
    """
    Retrieve users
    """
    users = await user_crud.get_users(session, skip=skip, limit=limit)
    return UsersPublic(
        data=[UserPublic.model_validate(user) for user in users],
        count=len(users),
    )

@router.get("/me", response_model=UserPublic)
async def read_current_user(
    session: SessionDep,
    current_user: CurrentUser,
) -> UserPublic:
    """
    Get current user
    """
    return UserPublic.model_validate(current_user)

@router.get("/{user_id}", response_model=UserPublic)
async def read_user(
    session: SessionDep,
    user_id: uuid.UUID,
) -> UserPublic:
    """
    Get user by ID
    """
    user = await user_crud.get_user(session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return UserPublic.model_validate(user)
