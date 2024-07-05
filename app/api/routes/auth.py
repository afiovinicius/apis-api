from datetime import datetime, timedelta
from pathlib import Path

import requests
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.libs.mails import send_email_background
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.crud import users as crud_users
from app.schemas import auth as auth_schema, user as user_schema

router = APIRouter(prefix="/auth", tags=["Autenticação"])

template_directory = Path(__file__).resolve().parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(template_directory))


@router.post("/signin-email", response_model=auth_schema.Token)
async def signin_email(
    request: Request,
    background_tasks: BackgroundTasks,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud_users.get_user_by_email(db, form_data.username)
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    user_agent = request.headers.get("user-agent")
    user_platform = request.headers.get("Sec-Ch-Ua-Platform")
    platform = f"{user_agent.split(' ')[0]} · {user_platform}"
    location = request.client.host
    time = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S (UTC)")

    subject = "Novo dispositivo autenticado"
    template_name = "signin-mail.html"
    context = {
        "request": request,
        "user_id": user.id,
        "username": user.name,
        "platform": platform,
        "location": location,
        "time": time,
    }
    body = templates.get_template(template_name).render(context)

    send_email_background(background_tasks, [user.email], subject, body)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/provider-google")
async def provider_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile&access_type=offline&prompt=consent"
    }


@router.get("/signin-google")
async def signin_google(code: str, db: Session = Depends(get_db)):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET_KEY,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=data)
    if not token_response.ok:
        raise HTTPException(
            status_code=token_response.status_code,
            detail="Failed to retrieve access token from Google",
        )
    access_token = token_response.json().get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Erro ao pega o acesso ao token",
        )
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if not user_info_response.ok:
        raise HTTPException(
            status_code=user_info_response.status_code,
            detail="Erro ao pegar os dados do usuário no google",
        )
    user_info = user_info_response.json()
    email = user_info.get("email")
    name = user_info.get("name")
    if not email or not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid user info received from Google",
        )
    email_user = crud_users.get_user_by_email(db, email)
    if not email_user:
        user_create = user_schema.UserCreate(
            email=email,
            name=name,
            password="",
            role="",
            is_provider_auth="google",
        )
        return crud_users.create_user(db, user_create)
    elif email_user.is_provider_auth != "google":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered with a different authentication method",
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info,
    }
