Возможности
Frontend (Vue)
- Список проектов с временем создания
- Создание проекта по названию
- Просмотр изображений проекта
- Загрузка изображений (кнопка и drag-and-drop)
- Просмотр изображения
- рисование прямоугольников мышью
- назначение/изменение класса
- удаление боксов
- подсказка при наведении
- список ранее использованных классов
- Аннотации в текущей версии хранятся локально в localStorage

Backend (FastAPI + PostgreSQL)
- Проекты:
- POST /projects — создать проект
- GET /projects — получить список проектов
- DELETE /projects/{id} — удалить проект и связанные изображения
- Изображения:
- POST /projects/{id}/images — загрузить 1+ изображений в проект
- GET /projects/{id}/images — получить метаданные и публичные ссылки
- DELETE /images/{image_id} — удалить изображение
- Публичная раздача файлов:
- GET /uploads/<storage_name> — доступ к загруженным изображениям по URL

Swagger: http://localhost:8000/docs

Технологии
- Frontend: Vue
- Backend: FastAPI и SQLAlchemy
- DB: PostgreSQL
- Контейнеризация: Docker и docker-compose

Запуск
Из корня репозитория:
docker-compose up --build

далее открыть ссылку:
http://localhost:8080
Swagger: http://localhost:8000/docs

закрытие
docker-compose down


Как перейти на S3/MinIO (план замены локального хранилища)
В проекте выделен слой хранения файлов backend/app/storage.py.
Сейчас он реализует локальное сохранение на диск:
save_upload_file(upload_dir, file) -> storage_name
delete_file(upload_dir, storage_name)

Чтобы перейти на MinIO/S3:
Заменить реализацию storage.py на работу с S3 API (boto3 / minio client).
Вместо storage_name хранить в БД ключ объекта (например bucket/key).
url в GET /projects/{id}/images формировать как публичный URL бакета.
Добавить сервис MinIO в docker-compose.yml

Архитектура API и таблиц при этом сохраняется: меняется только слой хранения файлов.