from pathlib import Path
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
    BackgroundTasks,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.api.libs.mails import send_email_background
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.schemas import auth as auth_schema
from app.crud import users as crud_users

router = APIRouter(prefix="/auth", tags=["Autenticação"])

template_directory = Path(__file__).resolve().parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(template_directory))


@router.post("/signin-with-email", response_model=auth_schema.Token)
async def signin_email(
    request: Request,
    background_tasks: BackgroundTasks,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud_users.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
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

    return {
        "access_token": access_token,
    }
