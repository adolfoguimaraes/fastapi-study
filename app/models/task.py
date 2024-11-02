from typing import  Annotated, List, Optional
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

class TaskModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    description: str = Field(...)
    date: str = Field(...)
    owner: Optional[int] = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders = {ObjectId: str},
        json_schema_extra={
            'example': {
                'title': 'Implementar funcionalidade de inserção de tarefas',
                'description': 'Implementar funcionalidade de inserção de tarefas',
                'date': '2024-11-02',
                'owner': 1
            }
        }
    )

class UpdateTaskModel(BaseModel):
    title: Optional[str] = Field(...)
    description: Optional[str] = Field(...)
    date: Optional[str] = Field(...)
    owner: Optional[int] = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            'example': {
                'title': 'Implementar funcionalidade de inserção de tarefas',
                'description': 'Implementar funcionalidade de inserção de tarefas',
                'date': '2024-11-02',
                'owner': 1
            }
        }
    )

class TaskCollection(BaseModel):
    tasks: List[TaskModel]