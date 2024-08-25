from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def get_user(
        db: Session, 
        user_id: int
):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(
        db: Session, 
        email: str
):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(
        db: Session, 
        user: schemas.UserCreate
):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_heart_data(
        db: Session,
        heart_data: schemas.HeartDiseaseInput, 
        prediction: int, user_id: int
):
    db_heart_data = models.HeartDisease(**heart_data.dict(), 
                                        target=prediction, user_id=user_id
                                        )
    db.add(db_heart_data)
    db.commit()
    db.refresh(db_heart_data)
    return db_heart_data

def get_heart_data(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        user_id: int = None
):
    query = db.query(models.HeartDisease)
    if user_id:
        query = query.filter(models.HeartDisease.user_id == user_id)
    return query.offset(skip).limit(limit).all()
