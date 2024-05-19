from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    validate_is_task_creator_or_superuser,
    validate_task_exist,
    validate_user_is_superuser
)
from app.core.config import configure_logger
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.task import task_crud
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead


router = APIRouter()
logger = configure_logger(__name__)


@router.post(
    '/',
    response_model=TaskRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    status_code=status.HTTP_201_CREATED
)
async def create_new_task(
        task: TaskCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Создать новую задачу."""
    try:
        task = await task_crud.create(
            obj_in=task,
            session=session,
            user=user
        )
        logger.info(f'Создана задача {task.id}')
        return task
    except Exception as e:
        await session.rollback()
        logger.error(f'Ошибка при создании задачи - {e}')
        raise e


@router.get(
    '/',
    response_model=List[TaskRead],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    status_code=status.HTTP_200_OK
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session),
    title: Optional[str] = Query(
        None,
        min_length=1,
        description=(
            'Название, или его часть, для'
            ' фильтрации задач по названию'
        )
    ),
    start_date: Optional[date] = Query(
        None,
        description=(
            'Начальная дата для фильтрации'
            ' задач по дате создания'
        )
    ),
    end_date: Optional[date] = Query(
        None,
        description=(
            'Конечная дата для фильтрации'
            ' задач по дате создания'
        )
    ),
):
    tasks = await task_crud.filter_tasks(
        session=session,
        title=title,
        start_date=start_date,
        end_date=end_date
    )
    return tasks


@router.get(
    '/{task_id}',
    response_model=TaskRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    status_code=status.HTTP_200_OK
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(
        get_async_session
    ),
):
    """Получить задачу."""
    task = await validate_task_exist(
        task_id=task_id,
        session=session
    )

    return task


@router.patch(
    '/{task_id}',
    response_model=TaskRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    status_code=status.HTTP_200_OK
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Изменить задачу."""

    task = await validate_task_exist(
        task_id=task_id,
        session=session
    )
    validate_is_task_creator_or_superuser(
        task=task,
        user=user
    )
    if task_update.creator_id:
        validate_user_is_superuser(
            user=user,
        )

    if task_update.finished:
        task_update['is_active'] = False
        task_update['close_date'] = datetime.now()
        logger.info(f'Задача {task.id} закрыта пользователем {user.id}')

    try:
        await task_crud.update(
            db_obj=task,
            obj_in=task_update,
            session=session,
        )
    except Exception as e:
        await session.rollback()
        logger.error(f'Ошибка при обновлении задачи - {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Ошибка при обновлении задачи - {str(e)}'
        )
    return task


@router.delete(
    '/{task_id}',
    response_model=TaskRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    status_code=status.HTTP_200_OK
)
async def delete_task(
    task_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить задачу."""
    task = await validate_task_exist(
        task_id=task_id,
        session=session
    )
    validate_is_task_creator_or_superuser(
        task=task,
        user=user
    )

    try:
        await task_crud.remove(
            db_obj=task,
            session=session,
        )
        logger.info(f'Задача {task.id} удалена пользователем {user.id}')
        return task
    except Exception as e:
        await session.rollback()
        logger.error(f'Ошибка при удалении задачи {task.id} - {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Ошибка при удалении задачи {task.id} - {str(e)}'
        )
