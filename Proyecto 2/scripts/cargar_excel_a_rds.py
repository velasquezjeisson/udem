import pandas as pd
import pyodbc
import requests
import io
import boto3
import os

# --- CONFIGURACIONES ---
DB_INSTANCE_IDENTIFIER = "tu-nombre-rds"  # <--- reemplaza con tu identificador de RDS
DB_NAME = "proyectodb"
DB_USER = "adminuser"
DB_PASSWORD = "StrongPassword123!"  # considera usar variables de entorno para seguridad
REGION = "us-east-1"  # ajusta según tu región

# --- OBTENER ENDPOINT DE RDS ---
rds = boto3.client('rds', region_name=REGION)
response = rds.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
endpoint = response['DBInstances'][0]['Endpoint']['Address']

print(f"✅ Endpoint de RDS obtenido: {endpoint}")

# --- DESCARGAR Y LEER EL EXCEL ---
url = "https://github.com/velasquezjeisson/udem/raw/refs/heads/master/Proyecto%202/MateriasPrimasConsolidado.xlsx"
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Error al descargar el archivo: {response.status_code}")

df = pd.read_excel(io.BytesIO(response.content))

# --- CONEXIÓN A RDS ---
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={endpoint},1433;"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)
cursor = conn.cursor()

# --- CREAR TABLA (debes ajustar esto a las columnas reales del Excel) ---
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='materias_primas' AND xtype='U')
CREATE TABLE materias_primas (
    Time_Stamp DATETIME,
    PV_Final FLOAT,
    -- agrega más columnas si es necesario
    PRIMARY KEY (Time_Stamp)
)
""")

# --- INSERTAR DATOS ---
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO materias_primas (Time_Stamp, PV_Final)
        VALUES (?, ?)
    """, row["Time_Stamp"], row["PV_Final"])

conn.commit()
cursor.close()
conn.close()

print("✅ Datos insertados correctamente en RDS.")
