#!/bin/bash

# Guardar salida en log
exec > /var/log/user_data.log 2>&1
set -x

# Actualizar sistema e instalar git
yum update -y
yum install -y git

# Ejecutar como ec2-user
sudo -u ec2-user -i <<'EOF'
cd /home/ec2-user

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar el repositorio o actualizarlo
if [ -d "udem/.git" ]; then
  cd udem
  git fetch origin
  git reset --hard origin/master
else
  git clone https://github.com/velasquezjeisson/udem.git
fi

# Entrar al proyecto (donde está pyproject.toml)
cd "/home/ec2-user/udem/Proyecto 2"

# Crear entorno virtual y sincronizar dependencias
uv venv
uv sync

# Ejecutar entrenamiento
cd src
../.venv/bin/python train.py

# Lanzar API con uvicorn
nohup ../.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
EOF
