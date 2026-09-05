import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT,
            priority TEXT,
            done INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_task(title, priority, deadline=None):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO tasks (title, deadline, priority, created_at) VALUES (?, ?, ?, ?)",
        (title, deadline, priority, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT id, title, deadline, priority FROM tasks WHERE done = 0"
    ).fetchall()
    conn.close()
    return rows

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def mark_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    def delete_task_by_title(title_keyword):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.execute(
        "SELECT id, title FROM tasks WHERE title LIKE ? AND done = 0",
        (f"%{title_keyword}%",)
    )
    matches = cursor.fetchall()
    if matches:
        task_id = matches[0][0]
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    conn.close()
    return matches[0][1] if matches else None

def mark_task_done(title_keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute(
        "SELECT id, title FROM tasks WHERE title LIKE ? AND done = 0",
        (f"%{title_keyword}%",)
    )
    matches = cursor.fetchall()
    if matches:
        task_id = matches[0][0]
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        conn.commit()
    conn.close()
    return matches[0][1] if matches else None

def delete_task_by_title(title_keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute(
        "SELECT id, title FROM tasks WHERE title LIKE ? AND done = 0",
        (f"%{title_keyword}%",)
    )
    matches = cursor.fetchall()
    if matches:
        task_id = matches[0][0]
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    conn.close()
    return matches[0][1] if matches else None

def mark_task_done(title_keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute(
        "SELECT id, title FROM tasks WHERE title LIKE ? AND done = 0",
        (f"%{title_keyword}%",)
    )
    matches = cursor.fetchall()
    if matches:
        task_id = matches[0][0]
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        conn.commit()
    conn.close()
    return matches[0][1] if matches else None