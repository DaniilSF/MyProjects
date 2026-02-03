from pydantic import BaseModel, Field
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

class ProjectOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class ImageOut(BaseModel):
    id: int
    project_id: int
    filename: str
    mime_type: str
    size: int
    created_at: datetime
    url: str

    class Config:
        from_attributes = True