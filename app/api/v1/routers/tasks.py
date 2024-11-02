from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, decode, DecodeError
from app.models.task import TaskCollection, TaskModel

from app.db import db_connection

from http import HTTPStatus

from app.security import validate_token

from app.exceptions import GeneralException, NotFoundException

router = APIRouter()

@router.get('/', 
    status_code=HTTPStatus.OK,
    response_model=TaskCollection,
    response_model_by_alias=False)
async def index(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):

    

    try:
        token_data = validate_token(token)

        if token_data.role != 'admin':
            tasks_db = await db_connection.db['tasks'].find({'owner': token_data.user_id}).to_list(1000)
        else:
            tasks_db = await db_connection.db['tasks'].find().to_list(1000)
         
        
        return TaskCollection(tasks=tasks_db)
    except Exception:
        raise GeneralException

@router.get('/{task_id}', 
    status_code=HTTPStatus.OK,
    response_description="Get task by id",
    response_model=TaskModel,
    response_model_by_alias=False)
async def get_task( 
    task_id: str,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
   
    token_data = validate_token(token)
    if token_data.role == 'admin':
        if (
            task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id)})
        ) is not None:
            return TaskModel(**task_db)

        raise NotFoundException
    else:
        if (
            task_db := await db_connection.db['tasks'].find_one({'_id': ObjectId(task_id), 'owner': token_data.user_id})
        ) is not None:
            return TaskModel(**task_db)

        raise NotFoundException
    
   
@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(
    task: TaskModel = Body(...),
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    try:
        token_data = validate_token(token)
        task.owner = token_data.user_id
        new_task = await db_connection.db['tasks'].insert_one(task.model_dump(by_alias=True, exclude=['id']))
        task_db = await db_connection.db['tasks'].find_one({'_id': new_task.inserted_id})
       
        return TaskModel(**task_db)
    except Exception as e:
        print(e)
        raise GeneralException
