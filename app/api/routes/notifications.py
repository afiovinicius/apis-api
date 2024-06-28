from fastapi import APIRouter, HTTPException, status

from app.api.libs.mails import track_click, track_open

router = APIRouter(prefix="/notifications", tags=["Notificações/Mensageria"])


@router.get("/tracking/open/{user_id}")
async def email_open_tracking(user_id: str):
    try:
        await track_open(user_id)
        return {"message": f"Usuário {user_id} visualizou o email!"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/tracking/click/{email}")
async def email_click_tracking(email: str):
    try:
        await track_click(email)
        return {"message": f"Clique no e-mail registrado para {email}"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
