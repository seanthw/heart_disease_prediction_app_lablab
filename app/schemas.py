from pydantic import BaseModel, EmailStr
from typing import Optional

class HeartDataBase(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

class HeartDataCreate(HeartDataBase):
    pass

class HeartData(HeartDataBase):
    id: int
    target: bool
    user_id: int

    class Config:
          from_attributes = True

class PredictionResult(BaseModel):
    prediction: float
    heart_disease_probability: float

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
         from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
