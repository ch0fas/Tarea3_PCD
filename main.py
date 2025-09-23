import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, conlist
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

import models
from database import engine, SessionLocal 

# === Starter Setup === #
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Users API", version='1.0.0')

# === Tables === #
models.Base.metadata.create_all(bind=engine)

# === Database Dependency === #
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# === Security === #
api_key_header = APIKeyHeader(name='X-API-KEY', description="API Key by header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Forbidden. Could not validate credentials")

# === DB Schema on Pydantic === #
class User(BaseModel):
    user_name: str = Field(min_length=1)
    user_email: str = Field(min_length=1)
    age: int = Field(gt=1, lt=2**31 - 1) # 32 bit integer limit
    recommendations: list[str] = Field(min_length=1)
    zip: str = Field(min_length=5, max_length=5) # In Mexico zip codes are, at most, 5 digits long.

# === Endpoints === #
@app.get('/')
def root():
    return {'RootMessage': 'API was setup! See docs for more info'}

@app.get('/api/v1/users/')
def list_users(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    return db.query(models.Users).all()

@app.post('/api/v1/users/')
def create_user(user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = models.Users(
        user_name = user.user_name,
        user_email = user.user_email,
        age = user.age,
        recommendations = user.recommendations,
        zip = user.zip
    )
    try:
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return user_model
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exist")

@app.put('/api/v1/users/{id}')
def update_user(id: int, user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.id == id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.zip = user.zip

    try:
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return {'deleted user by id': id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exist")


@app.delete('/api/v1/users/{id}')
def delete_user(id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.id == id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.query(models.Users).filter(models.Users.id == id).delete()
    db.commit()
    return {'Deleted user': id}
