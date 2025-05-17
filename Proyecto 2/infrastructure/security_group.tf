resource "aws_security_group" "ec2_sg" {
  name        = "${var.project_name}-ec2-sg"
  description = "Allow inbound traffic to EC2 and RDS"
  vpc_id      = aws_vpc.main.id

  # Microservicio FastAPI
  ingress {
    description = "Allow traffic to microservice port"
    from_port   = var.microservice_port
    to_port     = var.microservice_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Streamlit
  ingress {
    description = "Allow traffic to Streamlit port"
    from_port   = var.streamlit_port
    to_port     = var.streamlit_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH
  ingress {
    description = "Allow SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # ¡Restringe en producción!
  }

  # SQL Server entre recursos con el mismo SG
  ingress {
    description              = "Allow SQL Server access between EC2s and RDS"
    from_port                = 1433
    to_port                  = 1433
    protocol                 = "tcp"
    self                     = true
  }

  # Salida total
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
