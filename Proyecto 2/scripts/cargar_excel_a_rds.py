import pandas as pd
import pyodbc
import boto3
import os
import json

def get_db_credentials(secret_name="proyecto2/sqlserver-v2", region="us-east-1"):
    client = boto3.client("secretsmanager", region_name=region)
    secret = client.get_secret_value(SecretId=secret_name)
    return json.loads(secret["SecretString"])

def safe_str(value):
    return str(value) if pd.notna(value) else None

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# --- Cargar credenciales desde Secrets Manager ---
creds = get_db_credentials()
DB_USER = creds["username"]
DB_PASSWORD = creds["password"]
DB_NAME = "proyectodb"
REGION = "us-east-1"

# --- Obtener endpoint de RDS ---
rds = boto3.client('rds', region_name=REGION)
response = rds.describe_db_instances()
endpoint = response['DBInstances'][0]['Endpoint']['Address']

print(f"✅ Endpoint de RDS obtenido: {endpoint}")

# --- Crear base de datos si no existe ---
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
cursor_master.close()
conn_master.close()
print(f"✅ Base de datos '{DB_NAME}' verificada o creada.")

# --- Leer archivo Excel local ---
excel_path = "/home/ec2-user/udem/Proyecto 2/MateriasPrimasConsolidado.xlsx"
df = pd.read_excel(excel_path)

# --- Conectarse a la base de datos creada ---
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={endpoint},1433;"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)
cursor = conn.cursor()

# Eliminar tabla si ya existe
cursor.execute("""
IF OBJECT_ID('materias_primas', 'U') IS NOT NULL
DROP TABLE materias_primas;
""")

# Crear tabla con estructura completa
cursor.execute("""
CREATE TABLE materias_primas (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Partida NVARCHAR(50),
    Solicitud NVARCHAR(50),
    SP_Activo_Final NVARCHAR(100),
    Valor_SP_Final FLOAT,
    PV_Final FLOAT,
    MateriaPrima NVARCHAR(100),
    Equipo NVARCHAR(100),
    Local_Timestamp DATETIME,
    Time_Stamp DATETIME,
    TimeStampDb DATETIME
)
""")

# Insertar datos de Excel
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO materias_primas (
            Partida, Solicitud, SP_Activo_Final, Valor_SP_Final,
            PV_Final, MateriaPrima, Equipo, Local_Timestamp,
            Time_Stamp, TimeStampDb
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    safe_str(row["Partida"]),
    safe_str(row["Solicitud"]),
    safe_str(row["SP_Activo_Final"]),
    safe_float(row["Valor_SP_Final"]),
    safe_float(row["PV_Final"]),
    safe_str(row["MateriaPrima"]),
    safe_str(row["Equipo"]),
    row["Local_Timestamp"] if pd.notna(row["Local_Timestamp"]) else None,
    row["Time_Stamp"] if pd.notna(row["Time_Stamp"]) else None,
    row["TimeStampDb"] if pd.notna(row["TimeStampDb"]) else None)


conn.commit()
cursor.close()
conn.close()

print("✅ Datos insertados correctamente en RDS.")
