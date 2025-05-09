import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import os
import boto3
import joblib
import tempfile
from typing import Optional


app = FastAPI(title="Predicción multi-período con GradientBoostingRegressor")

# Parámetros del modelo en S3
S3_BUCKET_NAME = os.environ.get("S3_MODEL_BUCKET", "udem-proyecto2")
S3_MODEL_KEY = os.environ.get("S3_MODEL_KEY", "modelos/modelo_gb.pkl")
LOCAL_MODEL_PATH = os.path.join(tempfile.gettempdir(), "modelo_gb.pkl")

model = None
s3_client = None

# Input con solo el número de periodos
class ForecastRequest(BaseModel):
    n_periods: int
    initial_values: Optional[list[float]] = None

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
        if request.initial_values is None:
            current_input = np.array([100.0] * 10).reshape(1, -1)
        elif len(request.initial_values) != 10:
            raise HTTPException(status_code=400, detail="Se requieren exactamente 10 valores si se envían.")
        else:
            current_input = np.array(request.initial_values).reshape(1, -1)

        # Aplicar log1p al input para mantener la coherencia con el entrenamiento
        current_input = np.log1p(current_input)

        results = []

        for _ in range(request.n_periods):
            pred_log = model.predict(current_input)[0]
            pred_real = float(np.expm1(pred_log))
            results.append(pred_real)

            # Shift y agregar la predicción (log1p) como nuevo input
            current_input = np.roll(current_input, -1)
            current_input[0, -1] = np.log1p(pred_real)

        return ForecastResponse(predictions=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {e}")




@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
