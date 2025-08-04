
from fastapi import FastAPI
from models import example_model  # Example import from models
from database import SessionLocal, engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from tsembwog backend"}
