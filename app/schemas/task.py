from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.core.config import settings
from app.schemas.user import UserTaskRepresentation


class TaskBase(BaseModel):
    """Базовая схема объекта Task."""

    title: Optional[str] = Field(
        None,
        title='Название задачи',
        min_length=settings.task_title_min_length,
        max_length=settings.task_title_max_length,
    )
    description: Optional[str] = Field(
        None,
        title='Описание задачи',
    )
    expiration_date: Optional[datetime] = Field(
        None,
        title='Ожидаемая дата завершения задачи'
    )

    class Config:
        title = 'Базовая схема задачи'


class TaskCreate(TaskBase):
    """Схема создания объекта Task."""

    title: str = Field(
        ...,
        title='Название задачи',
        min_length=settings.task_title_min_length,
        max_length=settings.task_title_max_length,
    )
    description: str = Field(
        None,
        title='Описание задачи',
    )

    responsibles: List[int] = Field(
        ...,
        title='Список ответственных за исполнение задачи',
        min_length=1
    )
    auditors: Optional[List[int]] = Field(
        default_factory=list,
        description='Список наблюдателей за исполнением задачи.'
    )

    class Config:
        from_attributes = True
        title = 'Схема создания задачи'
        extra = 'forbid'
        json_schema_extra = {
            'example': {
                'title': 'Название задачи',
                'description': 'Описание задачи',
                'expiration_date': '2024-01-01',
                'responsibles': [1, 2, 3],
                'auditors': [4, 5, 6]
            }
        }


class TaskRead(TaskBase):
    """Схема отображения объекта Task."""

    id: int = Field(
        ...,
        title='Идентификатор задачи',
        ge=1,
    )
    creator: UserTaskRepresentation = Field(
        ...,
        title='Постановщик задачи'
    )
    responsibles: List[UserTaskRepresentation] = Field(
        ...,
        title='Ответственные'
    )
    auditors: Optional[List[UserTaskRepresentation]] = Field(
        default_factory=List,
        title='Наблюдатели'
    )
    is_active: bool = Field(
        ...,
        title='Статус активности задачи'
    )
    create_date: datetime = Field(
        ...,
        title='Дата создания задачи',
    )
    update_date: datetime = Field(
        None,
        title='Дата обновления задачи',
    )
    close_date: Optional[datetime] = Field(
        None,
        title='Дата завершения задачи'
    )
    expiration_date: Optional[datetime] = Field(
        None,
        title='Дата истечения срока выполнения задачи',
    )

    class Config:
        from_attributes = True
        title = 'Схема отображения задачи'
        extra = 'forbid'
        json_schema_extra = {
            'example': {
                'id': 1,
                'title': 'Название задачи',
                'description': 'Описание задачи',
                'creator': {
                    'id': 1,
                    'email': 'user@example.com',
                },
                'responsibles': [
                    {
                        'id': 2,
                        'email': 'user2@example.com',
                    },
                    {
                        'id': 3,
                        'email': 'user3@example.com',
                    },
                ],
                'auditors': [
                    {
                        'id': 4,
                        'email': 'user4@example.com',
                    },
                    {
                        'id': 5,
                        'email': 'user5@example.com',
                    },
                ],
                'is_active': False,
                'create_date': '2024-01-01',
                'update_date': '2024-01-02',
                'close_date': '2024-01-03',
                'expiration_date': '2024-01-04',
            }
        }


class TaskUpdate(TaskBase):
    """Схема обновления объекта Task."""

    creator_id: int = Field(
        None,
        title='Постановщик задачи'
    )
    responsibles: Optional[List[int]] = Field(
        None,
        title='Список ответственных за исполнение задачи',
        min_length=1
    )
    auditors: Optional[List[int]] = Field(
        default_factory=list,
        description='Список наблюдателей за исполнением задачи.'
    )
    finished: Optional[bool] = Field(
        False,
        description='Статус активности задачи'
    )

    class Config:
        from_attributes = True
        title = 'Схема обновления задачи'
        extra = 'forbid'
        json_schema_extra = {
            'example': {
                'title': 'Новое название задачи',
                'description': 'Новое  описание задачи',
                'expiration_date': '2024-01-01',
                'creator_id': 4,
                'responsibles': [4, 5, 6],
                'auditors': [1, 2, 3],
                'finished': False
            }
        }
