# Terraform: AWS Data Refinery Infrastructure

provider "aws" {
  region = "us-east-1"
}

variable "project_name" {
  default = "aiops-refinery"
}

# 1. S3 Buckets
resource "aws_s3_bucket" "raw_data" {
  bucket_prefix = "${var.project_name}-raw-"
}

resource "aws_s3_bucket" "refined_data" {
  bucket_prefix = "${var.project_name}-refined-"
}

# 2. IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# 3. IAM Policy for S3 access and logging
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:GetObject", "s3:PutObject"]
        Effect = "Allow"
        Resource = [
          "${aws_s3_bucket.raw_data.arn}/*",
          "${aws_s3_bucket.refined_data.arn}/*"
        ]
      },
      {
        Action = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Effect = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# 4. Lambda Function
resource "aws_lambda_function" "refinery_func" {
  function_name = "${var.project_name}-refiner"
  role          = aws_iam_role.lambda_role.arn
  handler       = "refinery_lambda.lambda_handler"
  runtime       = "python3.10"
  
  # Note: The ZIP must be created manually or via a CI/CD pipeline
  filename      = "lambda_function_payload.zip" 

  environment {
    variables = {
      DEST_BUCKET = aws_s3_bucket.refined_data.id
    }
  }

  # Using a public Klayers for Pandas/Numpy to simplify setup
  layers = ["arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-pandas:6"]
}

# 5. S3 Trigger Permission
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.refinery_func.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw_data.arn
}

# 6. S3 Event Notification
resource "aws_s3_bucket_notification" "trigger" {
  bucket = aws_s3_bucket.raw_data.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.refinery_func.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}

output "raw_bucket_name" {
  value = aws_s3_bucket.raw_data.id
}

output "refined_bucket_name" {
  value = aws_s3_bucket.refined_data.id
}
