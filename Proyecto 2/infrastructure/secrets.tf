resource "aws_secretsmanager_secret" "sql_credentials" {
  name        = "proyecto2/sqlserver-v2"
  description = "Credenciales para SQL Server RDS"
  lifecycle {
    prevent_destroy = true
  }
  tags = {
    Name = "proyecto2/sqlserver"
  }
}

resource "aws_secretsmanager_secret_version" "sql_credentials_version" {
  secret_id     = aws_secretsmanager_secret.sql_credentials.id
  secret_string = jsonencode({
    username = "adminuser",
    password = var.db_password
  })
}
