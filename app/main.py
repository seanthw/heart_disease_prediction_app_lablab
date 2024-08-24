from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth, prediction

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, tags=["authentication"])
app.include_router(prediction.router, tags=["prediction"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
