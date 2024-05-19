from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.task import task_crud
from app.models.task import Task
from app.models.user import User


def validate_is_task_creator_or_superuser(
    user: User,
    task: Task,
):
    """Проверить, что пользователь создатель задачи или суперпользователь."""
    if user.id != task.creator_id and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Нельзя редактировать чужие задачи.'
        )


async def validate_task_exist(
    task_id: int,
    session: AsyncSession
) -> Optional[Task]:
    """
    Проверить, что задача с данным айди существует.
    Если да - вернуть задачу.
    """
    task = await task_crud.get(
        task_id=task_id,
        session=session
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача с данным id не найдена.'
        )
    return task


def validate_user_is_superuser(
    user: User
):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав для выполнения запроса.'
        )
