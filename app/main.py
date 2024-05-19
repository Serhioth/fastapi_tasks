from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings, configure_logger
from app.core.init_db import create_first_superuser
from app.api.routers import main_router

logger = configure_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Приложение запускается')
    await create_first_superuser()
    logger.info('Суперпользователь создан')
    yield

    logger.warning('Приложение остановлено')


app = FastAPI(
    title=settings.app_title,
    lifespan=lifespan,
)
app.include_router(main_router)
