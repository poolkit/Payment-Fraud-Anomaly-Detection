from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.predict_pipeline import PredictPipeline
from src.logger import logging
from src.exception import CustomException
import json

app = FastAPI()

class InputData(BaseModel):
    data: dict

@app.get("/")
async def root():
    return {"message": "Welcome to anomaly detection endpoint"}

@app.post("/predict")
async def predict(input_data: InputData):
    data = input_data.data

    try:
        prediction_pipeline = PredictPipeline(data)
        prediction = prediction_pipeline.predict()

    except Exception as e:
        raise e

    output = 0 if prediction==1 else 1
    return {"Output": output}


