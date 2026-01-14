from sqlalchemy.orm import Session
from fastapi import HTTPException

from server import models, schemas
from server.auth import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_scores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Score).order_by(models.Score.score.desc()).offset(skip).limit(limit).all()

def create_user_score(db: Session, score: schemas.ScoreCreate, user_id: int):
    db_score = models.Score(**score.dict(), owner_id=user_id)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score
