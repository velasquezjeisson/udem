#!/bin/bash

# Guardar la salida del script en un archivo de log
exec > /var/log/user_data.log 2>&1
set -x

# Actualizar paquetes del sistema
yum update -y

# Instalar git (curl ya viene con Amazon Linux 2023)
yum install -y git

# Ejecutar todo como ec2-user
sudo -u ec2-user -i <<'EOF'
cd /home/ec2-user

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar el repositorio si no existe
if [ ! -d "udem" ]; then
    git clone https://github.com/velasquezjeisson/udem.git
fi

# Entrar al proyecto raíz (donde está pyproject.toml)
cd "udem/Proyecto 2"

# Crear y sincronizar entorno virtual
uv venv
uv sync

# Entrar a src y lanzar el servidor usando el entorno del proyecto
cd src
nohup ../.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
EOF
