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
DB_NAME = "proyectodb"
REGION = "us-east-1"

# --- Obtener endpoint de la primera instancia RDS disponible ---
rds = boto3.client('rds', region_name=REGION)
response = rds.describe_db_instances()
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
conn_master.autocommit = True

cursor_master = conn_master.cursor()

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

# --- Conectarse a la base de datos creada ---
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
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Partida NVARCHAR(50),
    Solicitud NVARCHAR(50),
    SP_Activo_Final FLOAT,
    Valor_SP_Final FLOAT,
    PV_Final FLOAT,
    MateriaPrima NVARCHAR(100),
    Equipo NVARCHAR(100),
    Local_Timestamp DATETIME,
    Time_Stamp DATETIME,
    TimeStampDb DATETIME
)
""")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO materias_primas (
            Partida, Solicitud, SP_Activo_Final, Valor_SP_Final,
            PV_Final, MateriaPrima, Equipo, Local_Timestamp,
            Time_Stamp, TimeStampDb
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    row["Partida"], row["Solicitud"], row["SP_Activo_Final"], row["Valor_SP_Final"],
    row["PV_Final"], row["MateriaPrima"], row["Equipo"],
    row["Local_Timestamp"], row["Time_Stamp"], row["TimeStampDb"])


conn.commit()
cursor.close()
conn.close()

print("✅ Datos insertados correctamente en RDS.")
