import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import os
import boto3
import joblib
import tempfile

app = FastAPI(title="Predicción multi-período con GradientBoostingRegressor")

# Parámetros del modelo en S3
S3_BUCKET_NAME = os.environ.get("S3_MODEL_BUCKET", "udem-proyecto2")
S3_MODEL_KEY = os.environ.get("S3_MODEL_KEY", "modelos/modelo_gb.pkl")
LOCAL_MODEL_PATH = os.path.join(tempfile.gettempdir(), "modelo_gb.pkl")

model = None
s3_client = None

# Input con solo el número de periodos
class ForecastRequest(BaseModel):
    n_periods: int  # cuántos pasos o días a predecir

# Output con lista de predicciones
class ForecastResponse(BaseModel):
    predictions: list[float]

@app.on_event("startup")
async def load_model():
    global model, s3_client
    try:
        s3_client = boto3.client('s3')
        s3_client.download_file(S3_BUCKET_NAME, S3_MODEL_KEY, LOCAL_MODEL_PATH)
        model = joblib.load(LOCAL_MODEL_PATH)
        print("Modelo cargado desde S3")
    except Exception as e:
        print(f"Error cargando el modelo: {e}")
        model = None

@app.post("/predict", response_model=ForecastResponse)
async def predict(request: ForecastRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")

    try:
        n = request.n_periods
        # Este input inicial es ejemplo, normalmente deberías tener un último valor de entrada real
        last_known_input = np.array([[100.0]])  # Cambiar por tu última entrada real

        results = []
        current_input = last_known_input

        for _ in range(n):
            pred = model.predict(current_input)[0]
            results.append(float(pred))
            current_input = np.array([[pred]])  # usar predicción como nuevo input

        return ForecastResponse(predictions=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {e}")

@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
