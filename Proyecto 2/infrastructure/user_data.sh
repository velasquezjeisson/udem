#!/bin/bash
exec > /var/log/user_data.log 2>&1
set -x

yum update -y
yum install -y git curl

# Instalar uv para ec2-user
sudo -u ec2-user -i <<'EOF'
curl -LsSf https://astral.sh/uv/install.sh | sh

cd /home/ec2-user
git clone https://github.com/velasquezjeisson/udem.git
cd "udem/Proyecto 2/src"
uv sync
EOF
