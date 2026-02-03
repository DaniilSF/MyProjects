import os
import shutil
from uuid import uuid4
from fastapi import UploadFile

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def save_upload_file(upload_dir: str, file: UploadFile) -> str:
    """
    Сохраняет UploadFile на диск.
    Возвращает storage_name (имя файла в хранилище), которое пишем в БД.
    """
    ensure_dir(upload_dir)

    _, ext = os.path.splitext(file.filename or "")
    storage_name = f"{uuid4().hex}{ext.lower()}"
    full_path = os.path.join(upload_dir, storage_name)

    with open(full_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    return storage_name

def delete_file(upload_dir: str, storage_name: str) -> None:
    full_path = os.path.join(upload_dir, storage_name)
    try:
        os.remove(full_path)
    except FileNotFoundError:
        pass