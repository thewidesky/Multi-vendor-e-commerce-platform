-- 随便先测试一下
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    rating FLOAT DEFAULT 0.0
);