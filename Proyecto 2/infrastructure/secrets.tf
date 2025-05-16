resource "aws_secretsmanager_secret" "sql_credentials" {
  name        = "proyecto2/sqlserver"
  description = "Credenciales para la instancia RDS SQL Server"
}

resource "aws_secretsmanager_secret_version" "sql_credentials_version" {
  secret_id     = aws_secretsmanager_secret.sql_credentials.id
  secret_string = jsonencode({
    username = "adminuser"
    password = var.db_password
  })
}
