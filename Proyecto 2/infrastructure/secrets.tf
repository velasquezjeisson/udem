resource "aws_secretsmanager_secret" "sql_credentials" {
  name        = "proyecto2/sqlserver-v2"  # ← cámbialo si el anterior está en pending deletion
  description = "Credenciales para la instancia RDS SQL Server"

  lifecycle {
    prevent_destroy = true  # ← impide que el secreto se destruya con `terraform destroy`
  }

  tags = {
    Name = "proyecto2/sqlserver"
  }
}
