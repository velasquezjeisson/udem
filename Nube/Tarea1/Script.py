

# %%
import boto3
import os
from dotenv import load_dotenv
from tkinter import Tk, filedialog

# %%
load_dotenv(dotenv_path='conf.env')


# %%
# Obtener las credenciales de las variables de entorno
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# %%
# Crear una sesión de boto3
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# %%
# Función para subir archivo a S3
def upload_file_to_s3(bucket_name, file_path):
    try:
        s3.upload_file(file_path, bucket_name, os.path.basename(file_path))
        print(f"Archivo {file_path} subido exitosamente a {bucket_name}")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")


# %%
# Seleccionar archivo usando Tkinter
def select_file():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal
    file_path = filedialog.askopenfilename()
    return file_path

# %%

if __name__ == "__main__":
    bucket_name = 'jeissonbucket2'
    file_path = select_file()
    if file_path:
        upload_file_to_s3(bucket_name, file_path)
    else:
        print("No se seleccionó ningún archivo.")


