-- schema.sql
-- 線上算命系統 SQLite 資料表結構

DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS lots;
DROP TABLE IF EXISTS users;

-- 1. 使用者 (users)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 籤詩 (lots)
CREATE TABLE lots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lot_number INTEGER NOT NULL,
    type TEXT,
    poem TEXT,
    explanation TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. 測算紀錄 (records)
CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lot_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (lot_id) REFERENCES lots (id) ON DELETE CASCADE
);
