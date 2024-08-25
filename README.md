# Heart Disease Prediction API

This repository contains a FastAPI-based API for predicting heart disease risk using machine learning.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/heart-disease-prediction.git
   cd heart-disease-prediction
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Ensure the `heart_disease_model.pkl` file is in the `backend/models/` directory.

2. Set up the database:
   - The application uses SQLite by default. The database file will be created automatically when you run the application for the first time.
   - If you want to use a different database, update the `DATABASE_URL` in `backend/app/database.py`.

3. (Optional) Set environment variables:
   - `SECRET_KEY`: Used for token encryption. If not set, a default value will be used.
   - `ALGORITHM`: JWT algorithm. Default is HS256.
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time. Default is 30 minutes.

## Running the Application

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Start the FastAPI server:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. The API will be available at `http://localhost:8000`.

## API Endpoints and Examples

### Register a New User

**Endpoint:** `POST /register`

**Example Request:**
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "strongpassword123"}'
```

**Example Response:**
```json
{
  "email": "user@example.com",
  "id": 1
}
```

### Obtain an Access Token

**Endpoint:** `POST /token`

**Example Request:**
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=strongpassword123"
```

**Example Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Make a Prediction

**Endpoint:** `POST /predict`

**Example Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 50,
       "sex": 1,
       "cp": 0,
       "trestbps": 140,
       "chol": 233,
       "fbs": 1,
       "restecg": 0,
       "thalach": 150,
       "exang": 0,
       "oldpeak": 2.3,
       "slope": 0,
       "ca": 0,
       "thal": 1
     }'
```

**Example Response:**
```json
{
  "prediction": 1,
  "probability": 0.75,
  "risk_category": "High",
  "message": "This prediction suggests a higher likelihood of heart disease. Please consult with a healthcare professional for proper evaluation and advice."
}
```

### Retrieve Prediction History

**Endpoint:** `GET /data`

**Example Request:**
```bash
curl -X GET "http://localhost:8000/data" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Example Response:**
```json
[
  {
    "id": 1,
    "age": 50,
    "sex": 1,
    "cp": 0,
    "trestbps": 140,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1,
    "target": 1,
    "user_id": 1
  }
]
```

## Dummy Data for Testing

You can use the following dummy data to test the prediction endpoint:

1. High Risk Case:
   ```json
   {
     "age": 65,
     "sex": 1,
     "cp": 2,
     "trestbps": 160,
     "chol": 280,
     "fbs": 1,
     "restecg": 2,
     "thalach": 130,
     "exang": 1,
     "oldpeak": 3.1,
     "slope": 2,
     "ca": 2,
     "thal": 3
   }
   ```

2. Low Risk Case:
   ```json
   {
     "age": 35,
     "sex": 0,
     "cp": 0,
     "trestbps": 120,
     "chol": 180,
     "fbs": 0,
     "restecg": 0,
     "thalach": 170,
     "exang": 0,
     "oldpeak": 0.5,
     "slope": 0,
     "ca": 0,
     "thal": 1
   }
   ```

3. Medium Risk Case:
   ```json
   {
     "age": 50,
     "sex": 1,
     "cp": 1,
     "trestbps": 140,
     "chol": 230,
     "fbs": 1,
     "restecg": 1,
     "thalach": 150,
     "exang": 0,
     "oldpeak": 1.5,
     "slope": 1,
     "ca": 1,
     "thal": 2
   }
   ```

## Understanding the Input Features

- `age`: Age in years
- `sex`: Sex (1 = male; 0 = female)
- `cp`: Chest pain type (0 = typical angina; 1 = atypical angina; 2 = non-anginal pain; 3 = asymptomatic)
- `trestbps`: Resting blood pressure (in mm Hg on admission to the hospital)
- `chol`: Serum cholesterol in mg/dl
- `fbs`: Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
- `restecg`: Resting electrocardiographic results (0 = normal; 1 = having ST-T wave abnormality; 2 = showing probable or definite left ventricular hypertrophy)
- `thalach`: Maximum heart rate achieved
- `exang`: Exercise induced angina (1 = yes; 0 = no)
- `oldpeak`: ST depression induced by exercise relative to rest
- `slope`: The slope of the peak exercise ST segment (0 = upsloping; 1 = flat; 2 = downsloping)
- `ca`: Number of major vessels (0-3) colored by fluoroscopy
- `thal`: 1 = normal; 2 = fixed defect; 3 = reversable defect

## API Documentation

FastAPI provides automatic interactive API documentation. Once the server is running, you can access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

To run the tests:

```
pytest
```

## License

[Include your chosen license here]

## Contributing

[Include guidelines for contributing to your project]

## Support

If you encounter any problems or have any questions, please open an issue in the GitHub repository.
