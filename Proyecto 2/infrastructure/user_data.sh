#!/bin/bash
yum update -y

# Install Git
yum install git -y

# Install curl
yum install curl -y

# Install uv 
sudo -u ec2-user -i -- bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'

# Clone repository
git clone https://github.com/velasquezjeisson/udem.git
cd "Proyecto 2/src"
uv sync
