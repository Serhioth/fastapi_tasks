from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[int], BaseModel):
    """Базовый класс для получения пользователя."""

    pass


class UserCreate(schemas.BaseUserCreate, BaseModel):
    """Базовый класс для создания пользователя."""

    class Config:
        exclude = ['is_superuser', 'is_verified']


class UserUpdate(schemas.BaseUserUpdate, BaseModel):
    """Базовый класс для изменения пользователя."""

    pass


class UserTaskRepresentation(BaseModel):
    """Класс для отображения информации о пользователе в задаче."""

    id: int
    email: EmailStr
