from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/auth/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return auth.register_user(db, user)

@app.post("/auth/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    result = auth.login_user(db, user)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result

@app.post("/todos", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = auth.get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_todo = models.Todo(title=todo.title, user_id=user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=List[schemas.TodoResponse])
def get_todos(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = auth.get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return db.query(models.Todo).filter(models.Todo.user_id == user.id).all()