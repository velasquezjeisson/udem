data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_s3_role" {
  name               = "${var.project_name}-ec2-s3-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# 🔄 Política combinada: S3 + DescribeInstances + DescribeLoadBalancers
data "aws_iam_policy_document" "combined_policy" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.app_bucket.arn,
      "${aws_s3_bucket.app_bucket.arn}/*"
    ]
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

resource "aws_iam_policy" "combined_access_policy" {
  name        = "${var.project_name}-ec2-full-access-policy"
  description = "Policy for S3, EC2 DescribeInstances, and ELB DescribeLoadBalancers"
  policy      = data.aws_iam_policy_document.combined_policy.json
}

resource "aws_iam_role_policy_attachment" "ec2_combined_attach" {
  role       = aws_iam_role.ec2_s3_role.name
  policy_arn = aws_iam_policy.combined_access_policy.arn
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile-2"
  role = aws_iam_role.ec2_s3_role.name
}

resource "aws_iam_role_policy" "allow_read_sql_secret" {
  name = "AllowReadSqlSecret"
  role = aws_iam_role.ec2_s3_role.id  # ← este es el nombre correcto

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
}



