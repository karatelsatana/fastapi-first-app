from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db, UserModel
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
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserModel(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"сообщение": f"Пользователь {user.name}, {user.age} лет сохранен в базе"}

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@app.get("/user/{user_id}")
def get_id(user_id: int, db: Session = Depends((get_db))):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"сообщение": f"Пользователь {user_id} удален"}

@app.put("/user/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db_user.name = user.name
    db_user.age = user.age
    db.commit()
    return {"id": user_id, "name": user.name, "age": user.age}  