from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.email_service.auth import send_new_account_email
from app.models.user import Role

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    with_archived: bool = False,
    _: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    ADMIN: Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit, with_archived=with_archived)
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    role: Role = Role.CUSTOMER,
    _: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    ADMIN: Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in, role=role)
    background_tasks.add_task(
        send_new_account_email,
        email_to=user_in.email,
        username=user_in.email,
        password=user_in.password,
    )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update current user.
    """
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Read current user.
    """
    return current_user


@router.delete("/me/archive", response_model=schemas.User)
def archive_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Archive the current user. Only admin users can unarchive users.
    """
    user = crud.user.archive(db, obj=current_user)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    ADMIN: Read a specific user by id.
    """
    user = crud.user.get(db, id=user_id, with_archived=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    if user == current_user:
        return user
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    user_in: schemas.UserUpdate,
    _: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    ADMIN: Update a user.
    """
    user = crud.user.get(db, id=user_id, with_archived=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with the requested id, does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}/archive", response_model=schemas.User)
def archive_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    _: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    ADMIN: Soft delete a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with requested id, does not exist in the system",
        )
    user = crud.user.archive(db, user)
    return user


@router.put("/{user_id}/unarchive", response_model=schemas.User)
def unarchive_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    _: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    ADMIN: Unarchive a user.
    """
    user = crud.user.get(db, id=user_id, with_archived=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with requested id, does not exist in the system",
        )
    user = crud.user.unarchive(db, user)
    return user


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    _: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    ADMIN: Permanently delete a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with requested id, does not exist in the system",
        )
    user = crud.user.remove(db, id=user_id)
    return user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user
