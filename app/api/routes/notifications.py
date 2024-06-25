from fastapi import APIRouter, HTTPException, status
from app.api.libs.mails import track_open, track_click

router = APIRouter(prefix="/notifications", tags=["Notificações/Mensageria"])


@router.get("/tracking/open/{token}")
async def email_open_tracking(token: str):
    try:
        await track_open(token)
        return {"message": f"Usuário {token} visualizou o email!"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/tracking/click/{token}")
async def email_click_tracking(token: str):
    try:
        await track_click(token)
        return {"message": f"Clique no e-mail registrado para {token}"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
