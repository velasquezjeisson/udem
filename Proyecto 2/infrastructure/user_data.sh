#!/bin/bash

# Guardar salida en log
exec > /var/log/user_data.log 2>&1
set -x

# Eliminar curl minimal si existe
yum remove -y curl-minimal || true

# Instalar dependencias necesarias
yum install -y git curl unzip

# Instalar uv como ec2-user
sudo -u ec2-user -i -- bash <<'EOF'
cd /home/ec2-user
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar el repositorio
git clone https://github.com/velasquezjeisson/udem.git

# Entrar al proyecto
cd "udem/Proyecto 2/src"

# Sincronizar dependencias
uv sync
EOF
