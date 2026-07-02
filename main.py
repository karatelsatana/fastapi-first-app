import sqlite3

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS users(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             age INTEGER NOT NULL
)
""")
conn.commit()
conn.close()


from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "работает"}

@app.get("/hello/{name}")
def greet(name: str):
    return {"message": f"Привет, {name}"}

@app.get("/user")
def get_user(name: str, age: int):
    return {"имя": name, "возраст": age}


from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.post("/user")
def create_user(user: User):
    conn = get_db()
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", (user.name, user.age))
    conn.commit()
    conn.close()
    return {"сообщение": f"Пользователь {user.name}, {user.age} лет сохранен в базе"}

@app.get("/users")
def list_users():
    conn = get_db()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/user/{user_id}")
def get_id(user_id: int):
    conn = get_db()
    number_id = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if number_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    conn.close()
    return dict(number_id)

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"сообщение": f"Пользователь {user_id} удален"}

@app.put("/user/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    conn.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (user.name, user.age, user_id))
    conn.commit()
    conn.close()
    return {"id": user_id, "name": user.name, "age": user.age}