import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_provider_auth = Column(String, default="email", nullable=False)

    role = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    last_logout = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    owned_tasks = relationship(
        "Task", back_populates="owner", foreign_keys="[Task.owner_id]"
    )
    assigned_tasks = relationship(
        "Task",
        back_populates="assigned_user",
        foreign_keys="[Task.assigned_user_id]",
    )

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
