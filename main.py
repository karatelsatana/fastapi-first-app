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


from fastapi import FastAPI

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