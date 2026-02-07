from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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

class AnnotationIn(BaseModel):
    x: float
    y: float
    w: float
    h: float
    class_name: str = Field(min_length=1, max_length=200)

class AnnotationOut(BaseModel):
    id: int
    image_id: int
    x: float
    y: float
    w: float
    h: float
    class_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class AnnotationsSave(BaseModel):
    annotations: list[AnnotationIn]

class PredictBoxOut(BaseModel):
    x: float
    y: float
    w: float
    h: float
    class_name: str

class PredictResponse(BaseModel):
    image_id: int
    boxes: list[PredictBoxOut]