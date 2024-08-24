import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from ..deps import get_current_user
import tensorflow as tf
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load the model
model_path = os.path.join(BASE_DIR, 'models', 'heart_disease_model.h5')

class LRTensorFlowOptimizerWrapper(tf.keras.optimizers.Optimizer):
    def __init__(self, optimizer):
        self.optimizer = optimizer

    def get_config(self):
        config = self.optimizer.get_config()
        if 'lr' in config:
            config['learning_rate'] = config.pop('lr')
        return config

    def __getattr__(self, name):
        return getattr(self.optimizer, name)

def load_model_with_custom_objects():
    custom_objects = {
        'LRTensorFlowOptimizerWrapper': LRTensorFlowOptimizerWrapper
    }
    with tf.keras.utils.custom_object_scope(custom_objects):
        model = tf.keras.models.load_model(model_path, compile=False)
    
    # Recompile the model with a new optimizer
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

try:
    model = load_model_with_custom_objects()
    logger.info("Model loaded successfully")
    logger.info(model.summary())
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

def preprocess_input(data: schemas.HeartDataBase):
    try:
        # Convert input data to numpy array
        input_data = np.array([[
            data.age, data.sex, data.cp, data.trestbps, data.chol, data.fbs,
            data.restecg, data.thalach, data.exang, data.oldpeak, data.slope,
            data.ca, data.thal
        ]])
        
        # Normalize the input data (adjust this based on how your model was trained)
        mean = np.mean(input_data, axis=0)
        std = np.std(input_data, axis=0)
        epsilon = 1e-8  # Small value to avoid division by zero
        
        normalized_data = np.where(std > epsilon, (input_data - mean) / (std + epsilon), 0)
        
        # Reshape the data to match the expected input shape (None, None, 13)
        reshaped_data = normalized_data.reshape((1, 1, 13))
        
        logger.info(f"Preprocessed input shape: {reshaped_data.shape}")
        logger.info(f"Preprocessed input: {reshaped_data}")
        
        return reshaped_data
    except Exception as e:
        logger.error(f"Error in preprocessing: {str(e)}")
        raise

@router.post("/predict", response_model=schemas.PredictionResult)
def predict_heart_disease(
    data: schemas.HeartDataBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        # Preprocess the input data
        preprocessed_data = preprocess_input(data)
        
        # Make prediction
        logger.info("Making prediction")
        prediction = model.predict(preprocessed_data)
        logger.info(f"Raw prediction: {prediction}")
        
        # Handle different possible output shapes
        if prediction.ndim > 1:
            prediction = prediction.flatten()
        
        prediction_value = float(prediction[0])
        logger.info(f"Final prediction value: {prediction_value}")
        
        # Create heart data entry in the database
        heart_data = crud.create_heart_data(db, data, prediction_value, current_user.id)
        
        return schemas.PredictionResult(
            prediction=prediction_value,
            heart_disease_probability=prediction_value,
            heart_data_id=heart_data.id
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/data", response_model=list[schemas.HeartData])
def get_user_heart_data(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_heart_data(db, skip=skip, limit=limit, user_id=current_user.id)
