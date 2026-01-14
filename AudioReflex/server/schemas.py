from pydantic import BaseModel
from typing import List, Optional

# --- Score Schemas ---
class ScoreBase(BaseModel):
    score: int

class ScoreCreate(ScoreBase):
    pass

class Score(ScoreBase):
    id: int
    owner_id: int
    owner: "User"

    class Config:
        orm_mode = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class UserWithScores(UserBase):
    id: int
    scores: List[Score] = []

    class Config:
        orm_mode = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
