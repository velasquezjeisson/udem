#!/bin/bash

# Guardar la salida del script en un archivo de log
exec > /var/log/user_data.log 2>&1
set -x

# Actualizar paquetes del sistema
yum update -y

# Instalar solo git (curl ya viene con la AMI de Amazon Linux 2023)
yum install -y git

# Ejecutar como ec2-user todo lo necesario para entorno local
sudo -u ec2-user -i <<'EOF'
cd /home/ec2-user

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar el repositorio (si ya existe, no volver a clonar)
if [ ! -d "udem" ]; then
    git clone https://github.com/velasquezjeisson/udem.git
fi

# Entrar a la carpeta del proyecto
cd "udem/Proyecto 2"

# Instalar dependencias desde pyproject.toml
uv sync

# Entrar a carpeta src y ejecutar el servidor FastAPI
cd src
source .venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
EOF
