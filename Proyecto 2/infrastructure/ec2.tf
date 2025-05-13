resource "aws_instance" "backend_servers" {
  count                     = 2  # cambia a cuántas instancias quieras
  ami                       = var.ami_id
  instance_type             = var.instance_type
  subnet_id                 = aws_subnet.public.id
  vpc_security_group_ids    = [aws_security_group.ec2_sg.id]
  iam_instance_profile      = aws_iam_instance_profile.ec2_profile.name
  user_data                 = file("user_data.sh")

  tags = {
    Name = "${var.project_name}-backend-${count.index}"
  }
}



resource "aws_instance" "frontend_server" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  user_data                   = file("user_data_front.sh")

  tags = {
    Name = "${var.project_name}-frontend"
  }
}
