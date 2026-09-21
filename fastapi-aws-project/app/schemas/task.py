from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100
    )

    description: str

    completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True