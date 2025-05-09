#!/bin/bash

# Guardar la salida del script en un archivo de log
exec > /var/log/user_data.log 2>&1
set -x

# Actualizar paquetes (opcional)
yum update -y

# Instalar solo git (curl ya viene con la AMI)
yum install -y git

# Ejecutar como ec2-user para que uv quede en su entorno
sudo -u ec2-user -i <<'EOF'
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar el repositorio
cd /home/ec2-user
git clone https://github.com/velasquezjeisson/udem.git

# Entrar a la carpeta del proyecto
cd "udem/Proyecto 2/src"

# Instalar dependencias declaradas en pyproject.toml
uv sync
EOF
