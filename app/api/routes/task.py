import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_active_user,
    get_current_admin_or_manager_user,
    get_current_user,
)
from app.core.database import get_db
from app.crud import tasks as crud_tasks
from app.schemas import task as task_schema, user as user_schema

router = APIRouter(prefix="/tasks", tags=["Atividades"])


@router.post(
    "/create",
    response_model=task_schema.Task,
    dependencies=[Depends(get_current_admin_or_manager_user)],
)
def create_task(
    task: task_schema.TaskCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    try:
        if current_user.role == "admin":
            task.owner_id = task.owner_id or current_user.id
            task.assigned_user_id = task.assigned_user_id or current_user.id
        elif current_user.role == "manager":
            task.owner_id = current_user.id
            task.assigned_user_id = task.assigned_user_id or current_user.id
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return crud_tasks.create_task(db=db, task=task)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/list",
    response_model=List[task_schema.Task],
    dependencies=[Depends(get_current_active_user)],
)
async def list_tasks(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_active_user),
):
    try:
        if current_user.role == "admin":
            tasks = crud_tasks.get_tasks(db, skip=skip, limit=limit)
        elif current_user.role == "manager":
            tasks = crud_tasks.get_tasks_for_manager(
                db, current_user.id, skip=skip, limit=limit
            )
        else:
            tasks = crud_tasks.get_tasks_for_member(
                db, current_user.id, skip=skip, limit=limit
            )

        return tasks
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/details/{task_id}",
    response_model=task_schema.Task,
    dependencies=[Depends(get_current_active_user)],
)
def details_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        db_task = crud_tasks.get_task(db, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put(
    "/edit/{task_id}",
    response_model=task_schema.Task,
    dependencies=[Depends(get_current_admin_or_manager_user)],
)
def update_task(
    task_id: uuid.UUID,
    task: task_schema.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    try:
        db_task = crud_tasks.get_task(db, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        if current_user.role == "admin" or current_user.id == db_task.owner_id:
            return crud_tasks.update_task(db=db, task_id=task_id, task=task)
        else:
            raise HTTPException(
                status_code=403, detail="Você não pode editar essa atividade."
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/delete/{task_id}",
    response_model=task_schema.Task,
    dependencies=[Depends(get_current_admin_or_manager_user)],
)
def delete_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user),
):
    try:
        db_task = crud_tasks.get_task(db, task_id=task_id)
        if db_task.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not enough permissions"
            )
        return crud_tasks.delete_task(db=db, task_id=task_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
