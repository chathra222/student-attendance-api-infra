locals {
  name="student-attendance"
}

module "aurora_mysql" {
  source = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 2.0"
  name              = "${local.name}-mysql"
  engine            = "aurora-mysql"
  engine_version    = "5.7.mysql_aurora.2.07.1"
  engine_mode       = "serverless"
  storage_encrypted = true
  backup_retention_period= 1
  vpc_id                = "vpc-1688536b"
  subnets               = ["subnet-b3a37182","subnet-5f92d351","subnet-047cdfa76a0bef73e"]
  create_security_group = true
  allowed_cidr_blocks   = ["172.31.0.0/16"]

  replica_scale_enabled = false
  replica_count         = 0

  #monitoring_interval = 60

  apply_immediately   = true
  skip_final_snapshot = true

  db_parameter_group_name         = aws_db_parameter_group.example_mysql.id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.example_mysql.id
  # enabled_cloudwatch_logs_exports = # NOT SUPPORTED

  scaling_configuration = {
    auto_pause               = true
    min_capacity             = 1
    max_capacity             = 2
    seconds_until_auto_pause = 300
    timeout_action           = "ForceApplyCapacityChange"
  }
}

resource "aws_db_parameter_group" "example_mysql" {
  name        = "${local.name}-aurora-db-mysql-parameter-group"
  family      = "aurora-mysql5.7"
  description = "${local.name}-aurora-db-mysql-parameter-group"
 # tags        = local.tags
}

resource "aws_rds_cluster_parameter_group" "example_mysql" {
  name        = "${local.name}-aurora-mysql-cluster-parameter-group"
  family      = "aurora-mysql5.7"
  description = "${local.name}-aurora-mysql-cluster-parameter-group"
#  tags        = local.tags
}