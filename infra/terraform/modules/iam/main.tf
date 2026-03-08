##############################################################################
# Datos locales
##############################################################################

locals {
  prefix = "flight-${var.environment}"

  default_tags = merge(var.tags, {
    Project     = "flight-reservation-system"
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

##############################################################################
# Datos del caller
##############################################################################

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

##############################################################################
# IRSA - Trust Policy para flight-api
##############################################################################

data "aws_iam_policy_document" "api_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [var.eks_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.eks_oidc_provider_url}:sub"
      values   = ["system:serviceaccount:${var.namespace}:flight-api"]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.eks_oidc_provider_url}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

##############################################################################
# IRSA - Trust Policy para flight-worker
##############################################################################

data "aws_iam_policy_document" "worker_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [var.eks_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.eks_oidc_provider_url}:sub"
      values   = ["system:serviceaccount:${var.namespace}:flight-worker"]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.eks_oidc_provider_url}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

##############################################################################
# Policy - Acceso a RDS (conexion via IAM Auth)
##############################################################################

data "aws_iam_policy_document" "rds_access" {
  statement {
    sid    = "RDSConnect"
    effect = "Allow"
    actions = [
      "rds-db:connect",
    ]
    resources = [
      "arn:aws:rds-db:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:dbuser:*/${local.prefix}-db-user",
    ]
  }
}

resource "aws_iam_policy" "rds_access" {
  name   = "${local.prefix}-rds-access"
  policy = data.aws_iam_policy_document.rds_access.json
  tags   = local.default_tags
}

##############################################################################
# Policy - Acceso a ElastiCache (Redis)
##############################################################################

data "aws_iam_policy_document" "elasticache_access" {
  statement {
    sid    = "ElastiCacheConnect"
    effect = "Allow"
    actions = [
      "elasticache:Connect",
    ]
    resources = [
      "arn:aws:elasticache:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:replicationgroup:${local.prefix}-redis",
      "arn:aws:elasticache:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:user:*",
    ]
  }
}

resource "aws_iam_policy" "elasticache_access" {
  name   = "${local.prefix}-elasticache-access"
  policy = data.aws_iam_policy_document.elasticache_access.json
  tags   = local.default_tags
}

##############################################################################
# Policy - Acceso a SQS (alternativa a RabbitMQ en AWS)
##############################################################################

data "aws_iam_policy_document" "sqs_access" {
  statement {
    sid    = "SQSSendReceive"
    effect = "Allow"
    actions = [
      "sqs:SendMessage",
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:GetQueueUrl",
    ]
    resources = [
      "arn:aws:sqs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${local.prefix}-*",
    ]
  }
}

resource "aws_iam_policy" "sqs_access" {
  name   = "${local.prefix}-sqs-access"
  policy = data.aws_iam_policy_document.sqs_access.json
  tags   = local.default_tags
}

##############################################################################
# Policy - S3 lectura (para assets / config)
##############################################################################

data "aws_iam_policy_document" "s3_readonly" {
  statement {
    sid    = "S3ReadOnly"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::${local.prefix}-assets",
      "arn:aws:s3:::${local.prefix}-assets/*",
    ]
  }
}

resource "aws_iam_policy" "s3_readonly" {
  name   = "${local.prefix}-s3-readonly"
  policy = data.aws_iam_policy_document.s3_readonly.json
  tags   = local.default_tags
}

##############################################################################
# Policy - CloudWatch Logs (solo para worker)
##############################################################################

data "aws_iam_policy_document" "cloudwatch_logs" {
  statement {
    sid    = "CloudWatchLogs"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams",
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/eks/${local.prefix}/*",
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/eks/${local.prefix}/*:log-stream:*",
    ]
  }
}

resource "aws_iam_policy" "cloudwatch_logs" {
  name   = "${local.prefix}-cloudwatch-logs"
  policy = data.aws_iam_policy_document.cloudwatch_logs.json
  tags   = local.default_tags
}

##############################################################################
# IAM Role - flight-api (IRSA)
##############################################################################

resource "aws_iam_role" "api" {
  name               = "${local.prefix}-api-irsa"
  assume_role_policy = data.aws_iam_policy_document.api_trust.json
  tags               = local.default_tags
}

resource "aws_iam_role_policy_attachment" "api_rds" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.rds_access.arn
}

resource "aws_iam_role_policy_attachment" "api_elasticache" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.elasticache_access.arn
}

resource "aws_iam_role_policy_attachment" "api_sqs" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.sqs_access.arn
}

resource "aws_iam_role_policy_attachment" "api_s3" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.s3_readonly.arn
}

##############################################################################
# IAM Role - flight-worker (IRSA)
##############################################################################

resource "aws_iam_role" "worker" {
  name               = "${local.prefix}-worker-irsa"
  assume_role_policy = data.aws_iam_policy_document.worker_trust.json
  tags               = local.default_tags
}

resource "aws_iam_role_policy_attachment" "worker_rds" {
  role       = aws_iam_role.worker.name
  policy_arn = aws_iam_policy.rds_access.arn
}

resource "aws_iam_role_policy_attachment" "worker_elasticache" {
  role       = aws_iam_role.worker.name
  policy_arn = aws_iam_policy.elasticache_access.arn
}

resource "aws_iam_role_policy_attachment" "worker_sqs" {
  role       = aws_iam_role.worker.name
  policy_arn = aws_iam_policy.sqs_access.arn
}

resource "aws_iam_role_policy_attachment" "worker_s3" {
  role       = aws_iam_role.worker.name
  policy_arn = aws_iam_policy.s3_readonly.arn
}

resource "aws_iam_role_policy_attachment" "worker_cloudwatch" {
  role       = aws_iam_role.worker.name
  policy_arn = aws_iam_policy.cloudwatch_logs.arn
}

##############################################################################
# CI/CD - Trust Policy para GitHub Actions (OIDC)
##############################################################################

data "aws_iam_policy_document" "cicd_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_org}/${var.github_repo}:*"]
    }
  }
}

##############################################################################
# Policy - CI/CD permisos (ECR push, EKS deploy, S3 state)
##############################################################################

data "aws_iam_policy_document" "cicd_ecr" {
  statement {
    sid    = "ECRAuth"
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
    ]
    resources = ["*"]
  }

  statement {
    sid    = "ECRPush"
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
    ]
    resources = [
      aws_ecr_repository.api.arn,
      aws_ecr_repository.frontend.arn,
    ]
  }
}

data "aws_iam_policy_document" "cicd_eks" {
  statement {
    sid    = "EKSDescribe"
    effect = "Allow"
    actions = [
      "eks:DescribeCluster",
      "eks:ListClusters",
    ]
    resources = [
      "arn:aws:eks:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:cluster/${local.prefix}-cluster",
    ]
  }
}

data "aws_iam_policy_document" "cicd_s3_state" {
  statement {
    sid    = "S3TerraformState"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket",
      "s3:DeleteObject",
    ]
    resources = [
      "arn:aws:s3:::${local.prefix}-terraform-state",
      "arn:aws:s3:::${local.prefix}-terraform-state/*",
    ]
  }

  statement {
    sid    = "DynamoDBStateLock"
    effect = "Allow"
    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:DeleteItem",
    ]
    resources = [
      "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${local.prefix}-terraform-lock",
    ]
  }
}

resource "aws_iam_policy" "cicd_ecr" {
  name   = "${local.prefix}-cicd-ecr"
  policy = data.aws_iam_policy_document.cicd_ecr.json
  tags   = local.default_tags
}

resource "aws_iam_policy" "cicd_eks" {
  name   = "${local.prefix}-cicd-eks"
  policy = data.aws_iam_policy_document.cicd_eks.json
  tags   = local.default_tags
}

resource "aws_iam_policy" "cicd_s3_state" {
  name   = "${local.prefix}-cicd-s3-state"
  policy = data.aws_iam_policy_document.cicd_s3_state.json
  tags   = local.default_tags
}

##############################################################################
# IAM Role - CI/CD (GitHub Actions)
##############################################################################

resource "aws_iam_role" "cicd" {
  name               = "${local.prefix}-cicd-github-actions"
  assume_role_policy = data.aws_iam_policy_document.cicd_trust.json
  tags               = local.default_tags
}

resource "aws_iam_role_policy_attachment" "cicd_ecr" {
  role       = aws_iam_role.cicd.name
  policy_arn = aws_iam_policy.cicd_ecr.arn
}

resource "aws_iam_role_policy_attachment" "cicd_eks" {
  role       = aws_iam_role.cicd.name
  policy_arn = aws_iam_policy.cicd_eks.arn
}

resource "aws_iam_role_policy_attachment" "cicd_s3_state" {
  role       = aws_iam_role.cicd.name
  policy_arn = aws_iam_policy.cicd_s3_state.arn
}

##############################################################################
# ECR Repositories
##############################################################################

resource "aws_ecr_repository" "api" {
  name                 = "${local.prefix}/flight-api"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = false

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = local.default_tags
}

resource "aws_ecr_repository" "frontend" {
  name                 = "${local.prefix}/flight-frontend"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = false

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = local.default_tags
}

##############################################################################
# ECR Lifecycle Policy - Mantener solo las ultimas 20 imagenes
##############################################################################

resource "aws_ecr_lifecycle_policy" "api" {
  repository = aws_ecr_repository.api.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Mantener solo las ultimas 20 imagenes"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 20
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_ecr_lifecycle_policy" "frontend" {
  repository = aws_ecr_repository.frontend.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Mantener solo las ultimas 20 imagenes"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 20
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
