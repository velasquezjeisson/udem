resource "aws_security_group" "ec2_sg" {
  name        = "${var.project_name}-ec2-sg"
  description = "Allow inbound traffic for microservice and all outbound traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description      = "Allow traffic to microservice port"
    from_port        = var.microservice_port
    to_port          = var.microservice_port
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    description      = "Allow traffic to Streamlit port"
    from_port        = var.streamlit_port
    to_port          = var.streamlit_port
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    description      = "Allow SSH access"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"] # WARNING: Allows SSH from anywhere. Restrict this in production.
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1" # Allow all outbound traffic
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-ec2-sg"
  }
}

resource "aws_security_group_rule" "allow_sqlserver_internal" {
  type                     = "ingress"
  from_port                = 1433
  to_port                  = 1433
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ec2_sg.id
  source_security_group_id = aws_security_group.ec2_sg.id

  description = "Allow SQL Server access within EC2 instances using the same SG"
}
