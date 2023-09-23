resource "random_password" "aurora" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = module.private_network.subnets.*.id
}

resource "aws_db_instance" "rds" {
  identifier             = "postgres"
  instance_class         = "db.t2.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "11.18"
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_groups.security_groups["rds"].id]
  username               = "postgres"
  password               = random_password.aurora.result
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.id
}

output "db_instance_endpt" {
  value = aws_db_instance.rds.endpoint
}
