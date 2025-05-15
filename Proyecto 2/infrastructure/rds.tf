resource "aws_db_instance" "sqlserver" {
  identifier              = "${var.project_name}-rds-sqlserver"
  engine                  = "sqlserver-ex"
  engine_version          = "15.00.4073.23.v1"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  max_allocated_storage   = 100
  storage_type            = "gp2"
  username                = "adminuser"
  password                = var.db_password
  db_name                 = "proyectodb"
  publicly_accessible     = true
  skip_final_snapshot     = true
  vpc_security_group_ids  = [aws_security_group.ec2_sg.id]
  db_subnet_group_name    = aws_db_subnet_group.main.name

  tags = {
    Name = "${var.project_name}-sqlserver"
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-subnet-group"
  subnet_ids = [aws_subnet.public.id]

  tags = {
    Name = "${var.project_name}-subnet-group"
  }
}
