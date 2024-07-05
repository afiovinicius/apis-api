import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.libs.redis import check_redis_connection
from app.api.routes import (
    admin as router_admin,
    auth as router_auth,
    notifications as router_notifications,
    task as router_task,
    user as router_user,
)
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Apis API",
    summary="API REST da Apis. Um webapp de produtividade que permite controle colaborativo das suas atividades e colegas.",
    description="""
        RBAC/ARBAC:
            Roles & Permissions.
        Roles:
            Admin
            Owner
            Manager
            Member
        Permissions:
            all_access
            view
            edit
            comment
        """,
    version="1.0.0",
    contact={
        "name": "Afio Vinícius",
        "url": "https://vicit.studio",
        "email": "afiovinicius@gmail.com",
    },
)

origins = [
    "https://www.apis.vicit.studio",
    "http://apis.vicit.studio",
    "https://apis.vicit.studio",
    "http://localhost",
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
