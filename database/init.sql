CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    description TEXT,
    img_url TEXT,
    img_local_path TEXT,
    img_s3_path TEXT,
    current_plate_number TEXT,
    old_plate_number TEXT,
    vehicle_color TEXT,
    voivodeship TEXT,
    city TEXT,
    source TEXT,
    roads JSONB,
    llm_extracted JSONB,
    car_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO cars (
    description,
    img_url,
    img_local_path,
    img_s3_path,
    current_plate_number,
    old_plate_number,
    vehicle_color,
    voivodeship,
    city,
    source,
    roads,
    llm_extracted,
    car_info
) VALUES (
    'test-image',
    'http://example.com/car.jpg',
    '/local/path/car.jpg',
    's3://bucket/car.jpg',
    'ABC12345',
    'XYZ98765',
    'Red',
    'Mazowieckie',
    'Warszawa',
    'camera1',
    '["A2", "S8"]',
    '{"status": "processed", "tags": ["car", "test"]}',
    'Toyota Corolla 2020'
);
