from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.references import (
    task_responsibles_reference,
    task_auditors_reference
)


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    created_tasks = relationship(
        'Task',
        back_populates="creator",
        foreign_keys="Task.creator_id"
    )
    tasks_as_auditor = relationship(
        'Task',
        secondary=task_auditors_reference,
        back_populates="auditors",
    )
    tasks_as_responsible = relationship(
        'Task',
        secondary=task_responsibles_reference,
        back_populates="responsibles",
    )
