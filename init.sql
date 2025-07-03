-- 1. Создание таблицы equipment (Оборудование)
CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    status VARCHAR(20),
    description TEXT
);

-- 2. Создание таблицы locations (Места погрузки/разгрузки)
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    coordinates VARCHAR(50)
);

-- 3. Создание таблицы distances (Расстояния между местами)
CREATE TABLE distances (
    id SERIAL PRIMARY KEY,
    location_from_id INTEGER REFERENCES locations(id),
    location_to_id INTEGER REFERENCES locations(id),
    distance_km NUMERIC(10,2) NOT NULL,
    estimated_time_min INTEGER,
    UNIQUE(location_from_id, location_to_id)
);

-- 4. Создание таблицы body_weights (Вес кузова)
CREATE TABLE body_weights (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER REFERENCES equipment(id),
    empty_weight_kg INTEGER NOT NULL,
    max_load_kg INTEGER NOT NULL,
    effective_date DATE
);

-- 5. Создание таблицы cargo_types (Типы груза)
CREATE TABLE cargo_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20),
    density_kg_m3 NUMERIC(10,2)
);

-- 6. Создание таблицы shipments (Отгрузки)
CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER REFERENCES equipment(id),
    cargo_type_id INTEGER REFERENCES cargo_types(id),
    load_location_id INTEGER REFERENCES locations(id),
    unload_location_id INTEGER REFERENCES locations(id),
    planned_datetime TIMESTAMP,
    actual_datetime TIMESTAMP,
    weight_kg INTEGER,
    status VARCHAR(20)
);

-- Заполнение equipment (10 машин)
INSERT INTO equipment (name, type, status, description) VALUES
('Кран КС-4571', 'Кран', 'Рабочий', 'Гусеничный кран, грузоподъемность 50т'),
('Грузовик Volvo FH16', 'Автомобиль', 'Рабочий', 'Седельный тягач, 600 л.с.'),
('Погрузчик CAT 950', 'Погрузчик', 'На ТО', 'Колесный погрузчик, ковш 3м3'),
('Бульдозер Komatsu D65', 'Бульдозер', 'Рабочий', 'Ширина отвала 4.2м'),
('Самосвал КамАЗ-6520', 'Автомобиль', 'Простой', 'Грузоподъемность 20т'),
('Экскаватор Hitachi ZX350', 'Экскаватор', 'Рабочий', 'Объем ковша 1.6м3'),
('Грузовик MAN TGS', 'Автомобиль', 'Рабочий', 'Седельный тягач, 440 л.с.'),
('Автокран Liebherr LTM 1050', 'Кран', 'На ТО', 'Грузоподъемность 50т'),
('Погрузчик JCB 457', 'Погрузчик', 'Рабочий', 'Вилочный погрузчик, 2.5т'),
('Бетоновоз SANY SY5250', 'Автомобиль', 'Рабочий', 'Объем миксера 8м3');

-- Заполнение locations (10 мест)
INSERT INTO locations (name, type, coordinates) VALUES
('Склад №1', 'Погрузка', '55.7522, 37.6156'),
('Карьер "Северный"', 'Погрузка', '55.9123, 37.4567'),
('Строительная площадка "Восток"', 'Разгрузка', '55.6345, 37.7123'),
('Склад стройматериалов', 'Погрузка', '55.7234, 37.8234'),
('ЖБИ завод', 'Погрузка', '55.8567, 37.9345'),
('Торговый центр "Южный"', 'Разгрузка', '55.6123, 37.7456'),
('ЖК "Новые высоты"', 'Разгрузка', '55.7890, 37.6789'),
('Порт "Речной"', 'Погрузка', '55.7345, 37.8567'),
('АЗС №45', 'Разгрузка', '55.8234, 37.7123'),
('Склад ГСМ', 'Разгрузка', '55.7123, 37.6234');

-- Заполнение distances (расстояния между местами)
INSERT INTO distances (location_from_id, location_to_id, distance_km, estimated_time_min) VALUES
(1, 3, 12.5, 25), (3, 1, 12.5, 25),
(2, 6, 18.3, 35), (6, 2, 18.3, 35),
(4, 7, 8.7, 15), (7, 4, 8.7, 15),
(5, 9, 22.1, 40), (9, 5, 22.1, 40),
(8, 10, 15.6, 30), (10, 8, 15.6, 30),
(1, 4, 5.2, 10), (4, 1, 5.2, 10),
(2, 5, 14.8, 28), (5, 2, 14.8, 28),
(3, 6, 9.3, 18), (6, 3, 9.3, 18),
(7, 10, 11.4, 22), (10, 7, 11.4, 22),
(8, 9, 7.9, 15), (9, 8, 7.9, 15);

-- Заполнение body_weights (вес кузова)
INSERT INTO body_weights (equipment_id, empty_weight_kg, max_load_kg, effective_date) VALUES
(2, 8000, 20000, '2025-01-01'),
(5, 12000, 20000, '2025-01-01'),
(6, 24000, 35000, '2025-01-01'),
(7, 7500, 18000, '2025-01-01'),
(10, 15000, 25000, '2025-01-01');

-- Заполнение cargo_types (5-10 типов груза)
INSERT INTO cargo_types (name, code, density_kg_m3) VALUES
('Щебень гранитный', 'SHB-001', 1500),
('Песок строительный', 'PES-002', 1600),
('Бетонные блоки', 'BET-003', 2300),
('Арматура А500С', 'ARM-004', 7850),
('Кирпич красный', 'KIR-005', 1800),
('Гравий', 'GRV-006', 1700),
('Цемент', 'CEM-007', 1300),
('Асфальт', 'ASF-008', 2400);

-- Заполнение shipments (20 отгрузок)
INSERT INTO shipments (equipment_id, cargo_type_id, load_location_id, unload_location_id, 
                      planned_datetime, actual_datetime, weight_kg, status) VALUES
(2, 1, 1, 3, '2025-06-25 08:00:00', '2025-06-25 08:15:00', 18000, 'Завершена'),
(5, 2, 2, 6, '2025-06-25 09:30:00', '2025-06-25 09:50:00', 15000, 'Завершена'),
(7, 3, 4, 7, '2025-06-25 10:15:00', NULL, 12000, 'В пути'),
(10, 4, 5, 9, '2025-06-26 07:00:00', NULL, 8000, 'Планируется'),
(2, 5, 1, 3, '2025-06-26 08:30:00', NULL, 17000, 'Планируется'),
(5, 6, 2, 6, '2025-06-25 14:00:00', '2025-06-25 14:25:00', 16000, 'Завершена'),
(7, 7, 4, 7, '2025-06-26 11:00:00', NULL, 10000, 'Планируется'),
(10, 8, 5, 9, '2025-06-25 16:30:00', '2025-06-25 16:50:00', 9000, 'Завершена'),
(2, 1, 8, 10, '2025-06-27 09:00:00', NULL, 19000, 'Планируется'),
(5, 2, 1, 3, '2025-06-25 12:00:00', '2025-06-25 12:20:00', 14000, 'Завершена'),
(7, 3, 2, 6, '2025-06-26 13:30:00', NULL, 11000, 'Планируется'),
(10, 4, 4, 7, '2025-06-27 10:00:00', NULL, 7500, 'Планируется'),
(2, 5, 5, 9, '2025-06-25 15:00:00', '2025-06-25 15:30:00', 16500, 'Завершена'),
(5, 6, 8, 10, '2025-06-26 14:00:00', NULL, 15500, 'Планируется'),
(7, 7, 1, 3, '2025-06-27 08:00:00', NULL, 9500, 'Планируется'),
(10, 8, 2, 6, '2025-06-25 17:00:00', '2025-06-25 17:25:00', 8500, 'Завершена'),
(2, 1, 4, 7, '2025-06-26 16:00:00', NULL, 17500, 'Планируется'),
(5, 2, 5, 9, '2025-06-27 11:30:00', NULL, 14500, 'Планируется'),
(7, 3, 8, 10, '2025-06-25 18:00:00', '2025-06-25 18:20:00', 10500, 'Завершена'),
(10, 4, 1, 3, '2025-06-26 15:00:00', NULL, 8200, 'Планируется');