import pandas as pd
import pyodbc
import requests
import io
import boto3
import os
import json


def get_db_credentials(secret_name="proyecto2/sqlserver-v2", region="us-east-1"):
    client = boto3.client("secretsmanager", region_name=region)
    secret = client.get_secret_value(SecretId=secret_name)
    return json.loads(secret["SecretString"])

# --- Cargar credenciales desde Secrets Manager ---
creds = get_db_credentials()
DB_USER = creds["username"]
DB_PASSWORD = creds["password"]
DB_INSTANCE_IDENTIFIER = "proyecto2-dev-rds-sqlserver"  # 👈 tu identificador real
DB_NAME = "proyectodb"
REGION = "us-east-1"

# --- Obtener el endpoint dinámicamente ---
rds = boto3.client('rds', region_name=REGION)
response = rds.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
endpoint = response['DBInstances'][0]['Endpoint']['Address']

print(f"✅ Endpoint de RDS obtenido: {endpoint}")

# --- Conectarse a base 'master' para crear base de datos ---
conn_master = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={endpoint},1433;"
    f"DATABASE=master;"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)
cursor_master = conn_master.cursor()

# Crear la base de datos si no existe
cursor_master.execute(f"""
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{DB_NAME}')
BEGIN
    CREATE DATABASE {DB_NAME};
END
""")
conn_master.commit()
cursor_master.close()
conn_master.close()
print(f"✅ Base de datos '{DB_NAME}' verificada o creada.")

# --- Descargar y leer el Excel ---
url = "https://github.com/velasquezjeisson/udem/raw/refs/heads/master/Proyecto%202/MateriasPrimasConsolidado.xlsx"
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Error al descargar el archivo: {response.status_code}")

df = pd.read_excel(io.BytesIO(response.content))

# --- Conectarse ahora a la base de datos creada ---
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={endpoint},1433;"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='materias_primas' AND xtype='U')
CREATE TABLE materias_primas (
    Time_Stamp DATETIME,
    PV_Final FLOAT,
    PRIMARY KEY (Time_Stamp)
)
""")

# Insertar los datos
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO materias_primas (Time_Stamp, PV_Final)
        VALUES (?, ?)
    """, row["Time_Stamp"], row["PV_Final"])

conn.commit()
cursor.close()
conn.close()

print("✅ Datos insertados correctamente en RDS.")
