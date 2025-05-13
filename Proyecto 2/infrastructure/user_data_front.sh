#!/bin/bash

# Guardar salida en log
exec > /var/log/user_data_front.log 2>&1
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

# Crear entorno virtual y sincronizar dependencias
cd "/home/ec2-user/udem/Proyecto 2"
uv venv
uv sync

# Lanzar solo el frontend
nohup .venv/bin/streamlit run app.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &
EOF
