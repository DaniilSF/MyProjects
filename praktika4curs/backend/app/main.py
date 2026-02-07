import os
import time
import random

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from sqlalchemy.exc import OperationalError

from .db import Base, engine, get_db
from .models import Project, Image, Annotation
from .schemas import ProjectCreate, ProjectOut, ImageOut, AnnotationOut, AnnotationsSave, PredictResponse, PredictBoxOut
from .storage import ensure_dir, save_upload_file, delete_file

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")

app = FastAPI(title="Projects Manager API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db_with_retries(max_tries: int = 30, sleep_seconds: float = 1.0) -> None:
    last_error = None
    for _ in range(max_tries):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as e:
            last_error = e
            time.sleep(sleep_seconds)
    raise last_error

@app.on_event("startup")
def on_startup():
    init_db_with_retries()
    ensure_dir(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    stmt = select(Project).order_by(Project.id.desc())
    return db.execute(stmt).scalars().all()

@app.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Project name is empty")
    project = Project(name=name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@app.delete("/projects/{id}", status_code=204)
def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for img in list(project.images):
        delete_file(UPLOAD_DIR, img.storage_name)
    db.delete(project)
    db.commit()
    return None

def image_to_out(request: Request, img: Image) -> ImageOut:
    url = str(request.base_url) + f"uploads/{img.storage_name}"
    return ImageOut(
        id=img.id,
        project_id=img.project_id,
        filename=img.filename,
        mime_type=img.mime_type,
        size=img.size,
        created_at=img.created_at,
        url=url,
    )

@app.post("/projects/{id}/images", response_model=list[ImageOut], status_code=201)
def upload_images(
    id: int,
    request: Request,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    ):
    project = db.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not files:
        raise HTTPException(status_code=400, detail="No files")
    created: list[ImageOut] = []

    for f in files:
        if not (f.content_type or "").startswith("image/"):
            raise HTTPException(status_code=400, detail=f"Not an image: {f.filename}")
        storage_name = save_upload_file(UPLOAD_DIR, f)
        img = Image(
            project_id=project.id,
            filename=f.filename or "image",
            mime_type=f.content_type or "application/octet-stream",
            size=0,
            storage_name=storage_name,
        )
        full_path = os.path.join(UPLOAD_DIR, storage_name)
        img.size = os.path.getsize(full_path)
        db.add(img)
        db.commit()
        db.refresh(img)
        created.append(image_to_out(request, img))
    return created

@app.get("/projects/{id}/images", response_model=list[ImageOut])
def list_images(id: int, request: Request, db: Session = Depends(get_db)):
    project = db.get(Project, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    stmt = select(Image).where(Image.project_id == id).order_by(Image.id.desc())
    images = db.execute(stmt).scalars().all()
    return [image_to_out(request, img) for img in images]

@app.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    img = db.get(Image, image_id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    delete_file(UPLOAD_DIR, img.storage_name)
    db.delete(img)
    db.commit()
    return None

@app.get("/images/{image_id}/annotations", response_model=list[AnnotationOut])
def get_annotations(image_id: int, db: Session = Depends(get_db)):
    img = db.get(Image, image_id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    stmt = select(Annotation).where(Annotation.image_id == image_id).order_by(Annotation.id.asc())
    return db.execute(stmt).scalars().all()

@app.post("/images/{image_id}/annotations", response_model=list[AnnotationOut], status_code=201)
def save_annotations(image_id: int, payload: AnnotationsSave, db: Session = Depends(get_db)):
    img = db.get(Image, image_id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    db.query(Annotation).filter(Annotation.image_id == image_id).delete()
    db.commit()
    created = []
    for a in payload.annotations:
        ann = Annotation(
            image_id=image_id,
            x=float(a.x),
            y=float(a.y),
            w=float(a.w),
            h=float(a.h),
            class_name=a.class_name.strip(),
        )
        db.add(ann)
        created.append(ann)
    db.commit()
    for ann in created:
        db.refresh(ann)
    return created

@app.delete("/annotations/{annotation_id}", status_code=204)
def delete_annotation(annotation_id: int, db: Session = Depends(get_db)):
    ann = db.get(Annotation, annotation_id)
    if not ann:
        raise HTTPException(status_code=404, detail="Annotation not found")
    db.delete(ann)
    db.commit()
    return None

@app.post("/predict/{image_id}", response_model=list[AnnotationOut], status_code=201)
def predict_fake(image_id: int, db: Session = Depends(get_db)):
    img = db.get(Image, image_id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    import random
    n = random.randint(1, 3)
    created = []
    for _ in range(n):
        w = random.uniform(0.10, 0.45)
        h = random.uniform(0.10, 0.45)
        x = random.uniform(0.0, 1.0 - w)
        y = random.uniform(0.0, 1.0 - h)
        cls = f"ML_obj_{random.randint(1, 10)}"
        ann = Annotation(
            image_id=image_id,
            x=float(x),
            y=float(y),
            w=float(w),
            h=float(h),
            class_name=cls,
        )
        db.add(ann)
        created.append(ann)
    db.commit()
    for a in created:
        db.refresh(a)
    return created