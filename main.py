from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db, UserModel
from fastapi import FastAPI, HTTPException
from auth import hash_password, verify_password, create_access_token
from auth import get_current_user

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

class UserRegister(BaseModel):
    name: str
    age: int
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class User(BaseModel):
    name: str
    age: int

class UserOut(BaseModel): #Для скрытия пароля/токена
    id: int
    name: str
    age: int

    class Config:
        from_attributes = True

@app.post("/user") #устаревший теперь ибо создали новый класс и создаем через него
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserModel(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"сообщение": f"Пользователь {user.name}, {user.age} лет сохранен в базе"}

@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    
    hashed_pw = hash_password(user.password)
    db_user = UserModel(name=user.name, age=user.age, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"сообщение": f"Пользователь {user.name} зарегистрирован"}

@app.get("/users", response_model=list[UserOut]) #Скрыли токен
def list_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
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

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.name == user.name).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверное имя или пароль")
    
    token = create_access_token({'sub': db_user.name})
    return {"access_token": token, "token_type": "bearer"}