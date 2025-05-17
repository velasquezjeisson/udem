resource "aws_security_group" "ec2_sg" {
  name        = "${var.project_name}-ec2-sg"
  description = "Allow inbound traffic to EC2 and RDS"
  vpc_id      = aws_vpc.main.id

  # Permite tráfico HTTP para FastAPI
  ingress {
    description      = "Allow traffic to microservice port"
    from_port        = var.microservice_port
    to_port          = var.microservice_port
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  # Permite acceso a Streamlit
  ingress {
    description      = "Allow traffic to Streamlit port"
    from_port        = var.streamlit_port
    to_port          = var.streamlit_port
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  # Permite SSH desde cualquier lugar (limitar en producción)
  ingress {
    description      = "Allow SSH access"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  # Salida total permitida
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-ec2-sg"
  }
}

# Regla explícita para permitir tráfico al puerto 1433 entre instancias con el mismo SG
resource "aws_security_group_rule" "allow_sqlserver_internal" {
  type                     = "ingress"
  from_port                = 1433
  to_port                  = 1433
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ec2_sg.id
  source_security_group_id = aws_security_group.ec2_sg.id
  description              = "Allow SQL Server access within EC2s using same SG"
}
