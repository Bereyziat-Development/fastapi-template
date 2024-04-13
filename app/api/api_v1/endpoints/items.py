from typing import Any, List

from fastapi import APIRouter, Depends
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.exceptions import HTTPItemNotFound, HTTPNotEnoughPermissions
from app.models import Role

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve items of the current user. Admin users retrieves all items.
    """
    if current_user.is_admin:
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_user(
            db, user=current_user, skip=skip, limit=limit
        )

    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new item. Admin cannot create an item for themselves. Use the dedicated admin endpoint instead.
    """
    item = crud.item.create_with_user(db=db, obj_in=item_in, user=current_user)
    return item


@router.post("/admin", response_model=schemas.Item)
def create_item_admin(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.require_role(Role.ADMIN)),
    user_id: UUID4,
) -> Any:
    """
    ADMIN: Create new item for another user.
    """
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPItemNotFound(current_user.language)
    item = crud.item.create_with_user(db=db, obj_in=item_in, user=user)
    return item


@router.put("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID4,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an item.
    """
    item = crud.item.get(db=db, id=id)
    if item is None:
        raise HTTPItemNotFound(current_user.language)
    if not current_user.is_admin and (item.user_id != current_user.id):
        raise HTTPNotEnoughPermissions(current_user.language)
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID4,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(db=db, id=id)
    if item is None:
        raise HTTPItemNotFound(current_user.language)
    if not current_user.is_admin and (item.user_id != current_user.id):
        raise HTTPNotEnoughPermissions(current_user.language)
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID4,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.item.get(db=db, id=id)
    if item is None:
        raise HTTPItemNotFound(current_user.language)
    if not current_user.is_admin and (item.user_id != current_user.id):
        raise HTTPNotEnoughPermissions(current_user.language)
    item = crud.item.remove(db, item)
    return item
