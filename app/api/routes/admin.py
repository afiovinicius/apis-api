from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import users as crud_users
from app.schemas import user as user_schema

router = APIRouter(
    prefix="/admin",
    tags=["Administrador"],
)


@router.post("/create-admin-user")
def create_admin_user(db: Session = Depends(get_db)):
    admin_user = crud_users.get_user_by_email(db, email="admin@vicit.studio")
    if admin_user:
        return {"message": "Admin user already exists"}

    admin_user_create = user_schema.UserCreate(
        email="admin@vicit.studio",
        name="Admin User",
        password="362514admin",
        role="admin",
    )
    admin_user = crud_users.create_user(db=db, user=admin_user_create)
    return admin_user
