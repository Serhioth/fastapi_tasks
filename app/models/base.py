from datetime import datetime

from sqlalchemy import Column, DateTime

from app.core.db import Base


class DBObject(Base):
    """Базовый класс для всех моделей базы данных, кроме пользователей."""

    __abstract__ = True

    create_date = Column(
        DateTime,
        nullable=False,
        default=datetime.now
    )
    update_date = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )
    close_date = Column(
        DateTime,
    )
