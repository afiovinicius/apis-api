import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.libs.redis import check_redis_connection
from app.core.database import engine, Base
from app.api.routes import (
    auth as router_auth,
    admin as router_admin,
    notifications as router_notifications,
    user as router_user,
    task as router_task,
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Manager",
    summary="Aplicação de gerenciamento de atividades com controle de acesso baseado em função (RBAC)",
    description="""
        RBAC:
            Roles & permissions.

        Roles:
            Admin
            Manager
            Member
        """,
    version="0.1.0",
    contact={
        "name": "Afio Vinícius",
        "url": "https://vicit.studio",
        "email": "afio@vicit.studio",
    },
)

origins = [
    "http://vicit.studio",
    "https://vicit.studio",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await check_redis_connection()


app.include_router(router_auth.router)
app.include_router(router_admin.router)
app.include_router(router_notifications.router)
app.include_router(router_user.router)
app.include_router(router_task.router)


@app.get("/", tags=["Padrão"])
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8080)
