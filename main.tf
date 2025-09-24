
resource "aws_lambda_function" "stop_instances" {
  filename         = "lambda-stop-function.zip"
  function_name    = var.lambda_stop_function_name
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("lambda-stop-function.zip")

  tags = {
    FreeTier = "yes"
  }
  
}

# Crear un archivo ZIP simple para Lambda
data "archive_file" "lambda_stop" {
  type        = "zip"
  output_path = "lambda-stop-function.zip"
  
  source {
    content  = <<-EOF
def lambda_handler(event, context):
    import boto3
    ec2 = boto3.client('ec2')
    
    # Parar instancias con tag AutoStop=true
    response = ec2.describe_instances(Filters=[
        {'Name': 'tag:AutoStop', 'Values': ['true']},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])
    
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    if instance_ids:
        ec2.stop_instances(InstanceIds=instance_ids)
        return f"Stopped instances: {instance_ids}"
    else:
        return "No instances to stop"
EOF
    filename = "index.py"
  }
}

# Rol IAM para Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda-stop-instances-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_ec2_stop" {
  name = "lambda-ec2-stop-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:StopInstances"
        ]
        Resource = "*"
      }
    ]
  })
}