from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, decode, DecodeError
from app.models.task import TaskCollection, TaskModel, UpdateTaskModel

from app.db.mongo_connection import db_connection

from http import HTTPStatus

from app.auth.security import  get_current_user

from app.exceptions import GeneralException, NotFoundException, SessionExpiredException


router = APIRouter()

@router.get('/', 
    status_code=HTTPStatus.OK,
    summary="Retrieve all tasks of the current user.",
    response_description="All tasks of the current user.",
    response_model=TaskCollection,
    response_model_by_alias=False)
async def index(
    limit: Optional[int] = 100,
    skip:  Optional[int] = 0,
    current_user: dict = Depends(get_current_user)
):
    """
        Retrieve all tasks of the current user.

        - `limit` (optional): The maximum number of tasks to return. Defaults to 100.
        - `skip` (optional): The number of tasks to skip. Defaults to 0.
        - Requires authentication with `JWT token`.
    """

    try:

        if current_user.role != 'admin':
            tasks_db = await db_connection.db['tasks'].find({'owner': current_user.user_id}).skip(skip).limit(limit).to_list()
        else:
            tasks_db = await db_connection.db['tasks'].find().skip(skip).limit(limit).to_list()
        
        return TaskCollection(tasks=tasks_db)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise GeneralException

@router.get('/{task_id}', 
    status_code=HTTPStatus.OK,
    summary="Retrieve a task by task_id.",
    response_description="A task by task_id.",
    response_model=TaskModel,
    response_model_by_alias=False)
async def get_task( 
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    
    """
        Retrieve a task by `task_id`.

        - `task_id` is required.
        - Requires authentication with `JWT token`.
    """
    
    if current_user.role == 'admin':
        if (
            task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id)})
        ) is not None:
            return TaskModel(**task_db)

        raise NotFoundException
    else:
        if (
            task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id), 'owner': current_user.user_id})
        ) is not None:
            return TaskModel(**task_db)

        raise NotFoundException
    
   
@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(
    task: TaskModel = Body(...),
    current_user: dict = Depends(get_current_user),
):
    try:
        task.owner = current_user.user_id
        new_task = await db_connection.db['tasks'].insert_one(task.model_dump(by_alias=True, exclude=['id']))
        task_db = await db_connection.db['tasks'].find_one({'_id': new_task.inserted_id})
       
        return TaskModel(**task_db)
    except Exception as e:
        print(e)
        raise GeneralException
    
@router.put('/{task_id}', status_code=HTTPStatus.OK)
async def update_task(
    task_id: str,
    task: UpdateTaskModel = Body(...),
    current_user: dict = Depends(get_current_user),
):
    

    task = {
        k: v for k, v in task.model_dump(by_alias=True).items() if v is not None
    }

    if len(task) > 0:

        if current_user.role == 'admin':
            if (
                task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id)})
            ) is not None:
                await db_connection.db['tasks'].update_one({'_id': ObjectId(task_id)}, {'$set': task})
            else:
                raise NotFoundException
        else:
            if (
                task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id), 'owner': current_user.user_id})
            ) is not None:
                await db_connection.db['tasks'].update_one({'_id': ObjectId(task_id)}, {'$set': task})
            else:
                raise NotFoundException
            
    if (
        task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id)})
    ) is not None:
        return TaskModel(**task_db)


@router.delete('/{task_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    
    if current_user.role == 'admin':
        if (
            task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id)})
        ) is not None:
            await db_connection.db['tasks'].delete_one({'_id': ObjectId(task_id)})
        else:
            raise NotFoundException
    else:
        if (
            task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id), 'owner': current_user.user_id})
        ) is not None:
            await db_connection.db['tasks'].delete_one({'_id': ObjectId(task_id)})
        else:
            raise NotFoundException

    