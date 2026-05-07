-- SQL 建表語法 (SQLite)

-- 1. 使用者表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT EXISTS UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'borrower', -- admin, borrower
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 書籍表
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    isbn TEXT,
    category TEXT,
    status TEXT NOT NULL DEFAULT 'Available', -- Available, Borrowed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. 借閱紀錄表
CREATE TABLE IF NOT EXISTS borrow_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    return_date DATETIME,
    status TEXT NOT NULL DEFAULT 'Active', -- Active, Returned
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
