from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    DateTime,
    String,
    Text,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import case

from app.models.base import DBObject
from app.models.references import (
    task_auditors_reference,
    task_responsibles_reference
)


class Task(DBObject):
    """Модель задачи."""

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    creator_id = Column(
        ForeignKey('user.id'),
        nullable=False
    )
    creator = relationship(
        "User",
        back_populates="created_tasks"
    )
    responsibles = relationship(
        'User',
        secondary=task_responsibles_reference,
        back_populates='tasks_as_responsible'
    )
    auditors = relationship(
        'User',
        secondary=task_auditors_reference,
        back_populates='tasks_as_auditor'
    )
    expiration_date = Column(DateTime, nullable=True)

    @hybrid_property
    def is_expired(self):
        """Проверить, что задача не просрочена через ORM."""
        return (
            self.expiration_date is not None
            and self.expiration_date < datetime.now()
        )

    @is_expired.expression
    def is_expired(cls):
        """Проверить, что задача не просрочена в SQL-запросе."""
        return case(
            [(cls.expiration_date == None, False)],  # noqa
            else_=datetime.now() > cls.expiration_date
        )

    def __repr__(self):
        return f'Задача {self.title}, постановщик - {self.creator_id}.'
