from fastapi import APIRouter

from app.api.endpoints import (
    task_router,
    user_router
)


main_router = APIRouter()

main_router.include_router(task_router, prefix='/tasks', tags=['tasks'])
main_router.include_router(user_router)
