from fastapi import APIRouter

from . import auth, tasks, users

router = APIRouter()
router.include_router(auth.router, prefix='/auth', tags=['auth'])
router.include_router(tasks.router, prefix='/tasks', tags=['tasks'])
router.include_router(users.router, prefix='/users', tags=['users'])