import pandas as pd
import pyodbc
import requests
import io

# Descargar el archivo Excel desde el enlace proporcionado
url = "https://github.com/velasquezjeisson/udem/raw/refs/heads/master/Proyecto%202/MateriasPrimasConsolidado.xlsx"
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Error al descargar el archivo: {response.status_code}")

# Leer el archivo Excel en un DataFrame de pandas
df = pd.read_excel(io.BytesIO(response.content))

# Conectar a la instancia RDS de SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tu_endpoint_rds,1433;"
    "DATABASE=proyectodb;"
    "UID=adminuser;"
    "PWD=StrongPassword123!"
)
cursor = conn.cursor()

# Crear la tabla si no existe (ajusta los tipos de datos según tu archivo Excel)
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='materias_primas' AND xtype='U')
CREATE TABLE materias_primas (
    columna1 VARCHAR(255),
    columna2 FLOAT,
    columna3 INT
    -- Agrega más columnas según sea necesario
)
""")

# Insertar los datos en la tabla
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO materias_primas (columna1, columna2, columna3)
        VALUES (?, ?, ?)
    """, row['columna1'], row['columna2'], row['columna3'])

# Confirmar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()
