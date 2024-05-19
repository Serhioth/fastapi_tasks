from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import configure_logger, settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


logger = configure_logger(__name__)


async def get_user_db(
    session: AsyncSession = Depends(
        get_async_session
    )
):
    """Получить пользователя из базы данных."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(
    tokenUrl='auth/jwt/login'
)


def get_jwt_strategy() -> JWTStrategy:
    """Настроить работу с JWT-токенами."""
    return JWTStrategy(
        secret=settings.jwt_secret,
        lifetime_seconds=settings.token_lifetime
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Класс для настройки аутентификации пользователей."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Валидировать парольт пользователя."""
        if len(password) < settings.password_min_length:
            raise InvalidPasswordException(
                reason=(
                    'Минимальная длина пароля - '
                    f'{settings.password_min_length} символов.')
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать Ваш email.'
            )

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None
    ):
        """Записать в логгере успешную регистрацию."""
        logger.info(
            f'Пользователь {user.email} зарегистрирован.'
        )


async def get_user_manager(
    user_db=Depends(
        get_user_db
    )
):
    """Получить объъект UserManager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True,
                                               superuser=True)
