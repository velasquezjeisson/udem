# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import sklearn
from sklearn.model_selection import train_test_split
from pathlib import Path
import subprocess
import json
import pyodbc
import boto3

# %%
def get_db_credentials(secret_name="proyecto2/sqlserver-v2", region="us-east-1"):
    client = boto3.client("secretsmanager", region_name=region)
    secret = client.get_secret_value(SecretId=secret_name)
    return json.loads(secret["SecretString"])

# --- Cargar credenciales desde Secrets Manager ---
creds = get_db_credentials()
DB_USER = creds["username"]
DB_PASSWORD = creds["password"]
DB_NAME = "proyectodb"
REGION = "us-east-1"

# --- Obtener endpoint RDS dinámicamente ---
rds = boto3.client('rds', region_name=REGION)
response = rds.describe_db_instances()
endpoint = response['DBInstances'][0]['Endpoint']['Address']

# Conexión a la base de datos
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={endpoint},1433;"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)
query = "SELECT * FROM materias_primas"
df = pd.read_sql(query, conn)
conn.close()

# %%
df = df.dropna(axis=0, how='any')
df = df.dropna(axis=1, how='any')
df = df.drop(axis=1, labels=[
    'Local_Timestamp','TimeStampDb','Partida','Solicitud',
    'Valor_SP_Final','SP_Activo_Final','MateriaPrima','Equipo'
])
df['Time_Stamp'] = pd.to_datetime(df['Time_Stamp'], dayfirst=True)
df.set_index('Time_Stamp', inplace=True)

# %%
df_diario = df.resample('D').sum()
df_filtrado = df_diario[df_diario["PV_Final"] > 0][["PV_Final"]]  # <-- solo PV_Final

# %%
retardo = 10
for i in range(1, retardo + 1):
    df_filtrado[f"PV_Final-{i}"] = df_filtrado["PV_Final"].shift(i)
df_filtrado.dropna(inplace=True)

# %%
X = df_filtrado.drop("PV_Final", axis=1)
y = df_filtrado["PV_Final"]

X_train = X.iloc[:-30]
X_test = X.iloc[-30:]
y_train = y.iloc[:-30]
y_test = y.iloc[-30:]

# %%
y_train_log = np.log1p(y_train)
y_test_log = np.log1p(y_test)
X_train_log = np.log1p(X_train)
X_test_log = np.log1p(X_test)

# %%
from sklearn.metrics import mean_absolute_percentage_error, make_scorer
mape_scorer = make_scorer(mean_absolute_percentage_error, greater_is_better=False)

# %%
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV

param_distributions_gb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'subsample': [0.7, 0.8, 1.0]
}

gb = GradientBoostingRegressor(random_state=42)

model_gb = RandomizedSearchCV(
    estimator=gb,
    param_distributions=param_distributions_gb,
    n_iter=30,
    scoring=mape_scorer,
    cv=5,
    n_jobs=-1,
    random_state=42,
    verbose=1
)

model_gb.fit(X_train_log, y_train_log)

print("Mejores parámetros:", model_gb.best_params_)
print(f"Score de validación cruzada (MAPE): {-model_gb.best_score_:.2f}%")
print(f"Score de entrenamiento (MAPE): {-model_gb.score(X_train_log, y_train_log):.2f}%")
print(f"Score de prueba (MAPE): {-model_gb.score(X_test_log, y_test_log):.2f}%")

y_pred_gb_log = model_gb.predict(X_test_log)
y_pred_gb = np.expm1(y_pred_gb_log)
mape_test_gb = mean_absolute_percentage_error(np.expm1(y_test_log), y_pred_gb)
print(f"MAPE real en prueba (escala original): {mape_test_gb * 100:.2f}%")

# Debug: verificar compatibilidad con el API
best_model = model_gb.best_estimator_
print("✅ Modelo entrenado con", best_model.n_features_in_, "features.")
print("✅ Nombres de features:", best_model.feature_names_in_)

# %%
import joblib
joblib.dump(best_model, "modelo_gb.pkl")

# %%
from dotenv import load_dotenv
load_dotenv(dotenv_path='conf.env')

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3')
bucket_name = 'udem-proyecto2'
s3_path = 'modelos/modelo_gb.pkl'

s3.upload_file('modelo_gb.pkl', bucket_name, s3_path)
print(f"📤 Modelo subido a s3://{bucket_name}/{s3_path}")
