from fastapi import FastAPI
from app.model import predict_lstm
from fastapi.responses import JSONResponse

app = FastAPI(title="Stock Prediction API")

@app.get("/")
def root():
    return {"message": "Welcome to the Stock Prediction API"}

@app.get("/predict-lstm")
def get_lstm_prediction():
    predictions, mse = predict_lstm()
    return JSONResponse(content={"predictions": predictions, "mse": mse})
