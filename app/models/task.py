from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    date: str
    owner: int