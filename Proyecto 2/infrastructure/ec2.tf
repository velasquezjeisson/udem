resource "aws_instance" "backend_servers" {
  count                     = 2  # cambia a cuántas instancias quieras
  ami                       = var.ami_id
  instance_type             = var.instance_type
  subnet_id                 = element([aws_subnet.public_a.id, aws_subnet.public_b.id], count.index % 2)
  vpc_security_group_ids    = [aws_security_group.ec2_sg.id]
  iam_instance_profile      = aws_iam_instance_profile.ec2_profile.name
  user_data                 = file("user_data.sh")
  depends_on = [aws_db_instance.sqlserver]  # ← Espera a que el RDS esté listo

  tags = {
    Name = "${var.project_name}-backend-${count.index}"
  }
}



resource "aws_instance" "frontend_server" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public_a.id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  user_data                   = file("user_data_front.sh")

  tags = {
    Name = "${var.project_name}-frontend"
  }
  depends_on = [aws_db_instance.sqlserver]

}
