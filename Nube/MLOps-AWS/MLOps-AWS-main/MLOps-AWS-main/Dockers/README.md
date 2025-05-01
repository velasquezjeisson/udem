# Docker Installation

https://docs.docker.com/desktop/

# Commands on Hands On

```
docker --version
docker run hello-world
docker pull busybox
docker images
docker run busybox
docker run busybox echo "hello from busybox mlops"
docker ps
docker ps -a
docker run -it busybox sh
docker rm <container_id>
```

# 2. Hands On

```

sudo yum update -y

# Instalar Git
sudo yum install git -y

# Instalar Docker
sudo yum install -y docker

# Iniciar el servicio de Docker
sudo service docker start

# Agregar el usuario ec2-user al grupo de docker para evitar usar sudo
sudo usermod -a -G docker ec2-user o sudo usermod -a -G docker $USER
sudo usermod -aG docker $USER

# Nos salimos de ec2 y nos volvemos a conectar
# Run hello-word
docker run hello-world

# Ver los contenedores que están actualmente en ejecución
docker ps

# Ver todos los contenedores
docker ps -a

# Git clone repo
git clone <HTTPS>

# Hacemos un build
docker build -t nombre-de-tu-imagen .

# Miramos las images disponibles
docker images

# Vamos a ec2 y editamos inbound rules Custom TCP 50000 0.0.0.0/0

# Docker run
docker run -d -p 5000:5000 nombre-de-tu-imagen

#Docker stop
docker stop <container_id>

#Docker run iteractive
docker run -it cats /bin/sh

```
