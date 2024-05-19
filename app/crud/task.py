from datetime import date
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import configure_logger
from app.crud.base import CRUDBase
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

logger = configure_logger(__name__)


class TaskCRUD(CRUDBase):
    """CRUD для объектов Task."""

    async def get(
        self,
        task_id: int,
        session: AsyncSession
    ) -> Task:
        """Получить задачу."""
        query = await session.execute(
            select(Task).options(
                selectinload(Task.responsibles),
                selectinload(Task.auditors)).where(Task.id == task_id)
        )
        task = query.scalars().first()
        return task

    async def create(
        self,
        obj_in: TaskCreate,
        user: User,
        session: AsyncSession
    ):
        """Создать задачу."""
        create_data = obj_in.model_dump()
        create_data["creator_id"] = user.id
        responsibles = create_data.pop('responsibles', [])
        auditors = create_data.pop('auditors', [])

        db_obj = self.model(**create_data)
        responsibles = await session.execute(
            select(User).where(User.id.in_(obj_in.responsibles))
        )
        responsibles = responsibles.scalars().all()
        for responsible_user in responsibles:
            db_obj.responsibles.append(responsible_user)

        if auditors:
            auditors = await session.execute(
                select(User).where(User.id.in_(obj_in.auditors))
            )
            auditors = auditors.scalars().all()
            for auditor_user in auditors:
                db_obj.auditors.append(auditor_user)

        session.add(db_obj)
        await session.commit()

        return await self.get(db_obj.id, session)

    async def update(
        self,
        db_obj: Task,
        obj_in: TaskUpdate,
        session: AsyncSession
    ):
        """Обновить существующую задачу."""
        update_data = obj_in.model_dump(exclude_unset=True)

        responsibles_ids = update_data.pop('responsibles')
        auditors_ids = update_data.pop('auditors')

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        if responsibles_ids is not None:
            new_responsibles = await session.execute(
                select(User).where(User.id.in_(responsibles_ids))
            )
            db_obj.responsibles[:] = new_responsibles.scalars().all()

        if auditors_ids is not None:
            new_auditors = await session.execute(
                select(User).where(User.id.in_(auditors_ids))
            )
            db_obj.auditors[:] = new_auditors.scalars().all()

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def filter_tasks(
        self,
        session: AsyncSession,
        title: Optional[str],
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> Optional[List[Task]]:
        """Отфильтровать задачи по заданным параметрам."""
        query = select(Task).options(
            selectinload(Task.responsibles),
            selectinload(Task.auditors),
        )

        if title:
            query = query.where(Task.title.ilike(f"%{title}%"))
        if start_date:
            query = query.where(Task.created_at >= start_date)
        if end_date:
            query = query.where(Task.created_at <= end_date)

        result = await session.execute(query)
        tasks = result.scalars().all()

        return tasks

    async def get_tasks_by_user_id(
        self,
        session: AsyncSession,
        user_id: int,
    ):
        """
        Получить все задачи, где создателем
        является заданный пользователь.
        """
        query = select(self.model).where(self.model.creator_id == user_id)

        result = await session.execute(query)

        return result.scalars().all()


task_crud = TaskCRUD(Task)
