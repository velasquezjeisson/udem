# Política de asunción para EC2
data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# Rol IAM para EC2
resource "aws_iam_role" "ec2_s3_role" {
  name               = "${var.project_name}-ec2-s3-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Política combinada para acceso a S3, EC2 y ELB
data "aws_iam_policy_document" "combined_policy" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket",
      "rds:DescribeDBInstances"
    ]
     resources = ["*"]
  }

  statement {
    actions = [
      "ec2:DescribeInstances"
    ]
    resources = ["*"]
  }

  statement {
    actions = [
      "elasticloadbalancing:DescribeLoadBalancers"
    ]
    resources = ["*"]
  }
}

# Política combinada como recurso adjunto
resource "aws_iam_policy" "combined_access_policy" {
  name        = "${var.project_name}-ec2-full-access-policy"
  description = "Policy for S3, EC2 DescribeInstances, and ELB DescribeLoadBalancers"
  policy      = data.aws_iam_policy_document.combined_policy.json
}

# Asociación de la política combinada al rol
resource "aws_iam_role_policy_attachment" "ec2_combined_attach" {
  role       = aws_iam_role.ec2_s3_role.name
  policy_arn = aws_iam_policy.combined_access_policy.arn
}

# Perfil de instancia para EC2
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile-2"
  role = aws_iam_role.ec2_s3_role.name
}

# Política adicional para permitir lectura de secretos de Secrets Manager
resource "aws_iam_role_policy" "allow_read_sql_secret" {
  name = "AllowReadSqlSecret"
  role = aws_iam_role.ec2_s3_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue"
        ],
        Resource = aws_secretsmanager_secret.sql_credentials.arn
      }
    ]
  })

  depends_on = [aws_secretsmanager_secret.sql_credentials]
}

resource "aws_iam_role_policy" "allow_cloudwatch_logs" {
  name = "AllowCloudWatchLogs"
  role = aws_iam_role.ec2_s3_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}
