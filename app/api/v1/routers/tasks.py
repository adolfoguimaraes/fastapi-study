from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import decode, DecodeError
from app.models.task import Task

from http import HTTPStatus

from app.security import validate_token

router = APIRouter()

all_taks = [
    {
        'id': 1,
        'title': 'Task 1',
        'description': 'Task 1 description',
        'date': '2022-01-01',
        'owner': 1
    },
    {	
        'id': 2,
        'title': 'Task 2',
        'description': 'Task 2 description',
        'date': '2022-01-01',
        'owner': 2
    }
]

@router.get('/', status_code=HTTPStatus.OK)
def index(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    response_model=[Task]
):

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = validate_token(token, credentials_exception)

        return_tasks = []

        for task in all_taks:
            if task['owner'] == token_data.user_id:
                return_tasks.append(task)

        return return_tasks

    except DecodeError:
        raise credentials_exception
