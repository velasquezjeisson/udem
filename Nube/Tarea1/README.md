# Script para subir archivos a Amazon S3

Este script en Python permite subir archivos a un bucket de Amazon S3 utilizando `boto3` y manejando las credenciales de forma segura.

## Requisitos

- Python 3.x
- `boto3`
- `python-dotenv`

## Instalación

1. Instala las dependencias:
    ```bash
    pip install boto3 python-dotenv
    ```

2. Crea un archivo `conf.env` en el directorio del proyecto y agrega tus credenciales de AWS:
    ```plaintext
    AWS_ACCESS_KEY_ID=tu_access_key_id
    AWS_SECRET_ACCESS_KEY=tu_secret_access_key
    ```

## Uso

1. Ejecuta el script:
    ```bash
    python script.py
    ```

2. Selecciona el archivo que deseas subir cuando se abra la ventana de selección de archivos.

3. El archivo será subido al bucket especificado y recibirás una confirmación en la consola.

