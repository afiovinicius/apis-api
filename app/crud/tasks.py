import uuid
from typing import List

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: str):
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Task).offset(skip).limit(limit).all()


def get_tasks_for_manager(
    db: Session, manager_id: uuid.UUID, skip: int = 0, limit: int = 10
) -> List[Task]:
    return (
        db.query(Task)
        .filter((Task.owner_id == manager_id) | (Task.assigned_user_id == manager_id))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_tasks_for_member(
    db: Session, member_id: uuid.UUID, skip: int = 0, limit: int = 10
) -> List[Task]:
    return (
        db.query(Task)
        .filter(Task.assigned_user_id == member_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: str, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        update_data = task.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: str):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
