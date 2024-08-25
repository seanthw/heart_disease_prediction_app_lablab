import os
import joblib
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import pandas as pd
from . import crud, models, schemas, auth
from .database import engine, SessionLocal
from .deps import get_current_user, get_db

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Load the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'models', 'heart_disease_model.pkl')

try:
    model = joblib.load(model_path)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}", exc_info=True)
    model = None

# Authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/predict")
async def predict(input: schemas.HeartDiseaseInput, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available. Please ensure the model is properly loaded.")
    
    input_data = pd.DataFrame([input.dict()])
    prediction_proba = model.predict_proba(input_data)[0]
    prediction = int(prediction_proba[1] > 0.5)
    
    result = {
        "prediction": prediction,
        "probability": float(prediction_proba[1]),
        "risk_category": "High" if prediction_proba[1] > 0.7 else "Medium" if prediction_proba[1] > 0.3 else "Low",
        "message": "This prediction suggests a higher likelihood of heart disease. Please consult with a healthcare professional for proper evaluation and advice." if prediction == 1 else "This prediction suggests a lower likelihood of heart disease. However, always maintain a healthy lifestyle and consult with healthcare professionals regularly."
    }
    
    # Save prediction to database
    crud.create_heart_data(db, input, prediction, current_user.id)
    
    return result

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/data", response_model=list[schemas.HeartData])
def get_user_heart_data(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_heart_data(db, skip=skip, limit=limit, user_id=current_user.id)
