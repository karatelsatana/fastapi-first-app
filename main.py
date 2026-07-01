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
    return {"сообщение": f"Пользователь {user.name}, {user.age} лет создан"}