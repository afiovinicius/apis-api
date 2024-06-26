import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.crud.users import get_user_by_email
from app.models.user import User
from app.api.routes.auth import oauth2_scheme


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.DATABASE_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


def get_current_manager_user(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


def get_current_admin_or_manager_user(
    current_user: User = Depends(get_current_active_user),
):
    allowed_roles = ["admin", "manager"]
    try:
        if current_user is None or current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not admin or manager",
            )
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
