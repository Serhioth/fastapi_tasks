from sqlalchemy import Column, ForeignKey, Table

from app.core.db import Base


# Таблица для сохранения many-to-many связей
# между задачей и ответственными за исполнение.
task_responsibles_reference = Table(
    "task_responsibles_reference",
    Base.metadata,
    Column('task_id', ForeignKey('task.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)

# Таблица для сохранения many-to-many связей
# между задачей и наблюдателями.
task_auditors_reference = Table(
    "task_auditors_reference",
    Base.metadata,
    Column('task_id', ForeignKey('task.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)
