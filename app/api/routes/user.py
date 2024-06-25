import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import users as crud_users
from app.schemas import user as user_schema
from app.api.dependencies import get_current_admin_user

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.post(
    "/add",
    response_model=user_schema.User,
    dependencies=[Depends(get_current_admin_user)],
)
def add_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud_users.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        return crud_users.create_user(db=db, user=user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/list",
    response_model=List[user_schema.User],
    dependencies=[Depends(get_current_admin_user)],
)
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    try:
        users = crud_users.get_users(db, skip=skip, limit=limit)
        return users
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/details/{user_id}",
    response_model=user_schema.User,
    dependencies=[Depends(get_current_admin_user)],
)
def details_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        db_user = crud_users.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put(
    "/edit/{user_id}",
    response_model=user_schema.User,
    dependencies=[Depends(get_current_admin_user)],
)
def update_user(
    user_id: uuid.UUID, user: user_schema.UserUpdate, db: Session = Depends(get_db)
):
    try:
        return update_user(db=db, user_id=user_id, user=user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/delete/{user_id}",
    response_model=user_schema.User,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        return delete_user(db=db, user_id=user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
