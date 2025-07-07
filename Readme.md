документация проекта «Dispatcher»

Инструкция по развертыванию

1. Требования к хост-машине:

> Docker >= 20.10 и Docker Compose V2 (в Docker Desktop уже встроен).
> Свободны порты 5432, 8000, 5173 (можно изменить в `docker-compose.yml`).
> Доступ в интернет при первом старте для загрузки базовых образов.

1.1) Скопируйте содержимое проекта в отдельную папку.

1.2) В каталоге, где лежит `docker-compose.yml`, выполните

   docker compose up --build
 *(Флаг `--build` гарантирует пересборку образов из исходников.)*

1.3) После завершения сборки и старта контейнеров:

| Сервис                   | URL на хосте                                           |Содержимое                                  |
|Frontend (Vue + Bootstrap)|[http://localhost:5173](http://localhost:5173)          |Веб-интерфейс диспетчеризации               |
|Backend (FastAPI)         |[http://localhost:8000/docs](http://localhost:8000/docs)|Swagger UI с документацией API              |
|PostgreSQL                | `localhost:5432` (user/password — `postgres`)          |База `dispatcher_ref_db` с тестовыми данными|

1.4) Остановить приложение:

   docker compose down
   *(добавьте `-v`, если нужно стереть данные Postgres, хранящиеся в томе `postgres_data`).*

---

2. Описание структуры БД

|Таблица      |Ключи                                              | Поля (тип, комментарий)                   |
|equipment    |`id` PK                                            |        ↓
`id` SERIAL, `name` varchar 100 NOT NULL, `type` varchar 50, `status` varchar 20, `description` text |

|locations    |`id` PK                                            |        ↓
`id` SERIAL, `name` varchar 100 NOT NULL, `type` varchar 20 NOT NULL («Погрузка» / «Разгрузка»), `coordinates` varchar 50 |

|distances    |`id` PK, `UNIQUE(location_from_id, location_to_id)`|        ↓
`location_from_id` FK → locations.id, `location_to_id` FK → locations.id, `distance_km` numeric 10,2 NOT NULL, `estimated_time_min` int |

|body_weights |`id` PK                                            |        ↓
`equipment_id` FK → equipment.id, `empty_weight_kg` int NOT NULL, `max_load_kg` int NOT NULL, `effective_date` date |

|cargo_types  |`id` PK                                            |        ↓
`name` varchar 100 NOT NULL, `code` varchar 20, `density_kg_m3` numeric 10,2 |

|shipments    | `id` PK                                           |        ↓
`equipment_id` FK → equipment.id, `cargo_type_id` FK → cargo\_types.id, `load_location_id` FK → locations.id, `unload_location_id` FK → locations.id, `planned_datetime` timestamp, `actual_datetime` timestamp, `weight_kg` int, `status` varchar 20 |

*Все внешние ключи настроены на `ON DELETE SET NULL`, поэтому сначала можно удалять связанные записи без нарушения целостности (при необходимости изменить это в `init.sql`).*

---

3. Основные функции веб-интерфейса

Веб-клиент построен как SPA (Vue 3 + Vue-Router 4) и использует компонент `<TableList>` для единообразного вывода. Навигация — верхнее меню.

| Вкладка                   | Что показывает                        | Особенности                                                |
|Оборудование (equipment)   |Список всех записей таблицы equipment  |Поиск по полям name, type, status                           |
|Места (locations)          |Перечень пунктов мест                  |Фильтрация строкой поиска (name, type)                      |
|Расстояния (distances)     |Таблица пар «Откуда → Куда» с дистанцией и временем |Отображаются названия мест, а не их ID         |
|Веса кузовов (body_weights)|Список записей из body_weights       |Колонка Оборудование берётся через JOIN, видна модель, а не FK|
|Типы груза (cargo_types)   |Каталог грузов                         |Поиск по name или code                                      |
|Отгрузки (shipments)       |Агрегированная таблица плана/факта перевозок |Благодаря selectinload на бекенде выводятся name      |

> интерфейс работает в режиме только-чтение