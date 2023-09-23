resource "aws_vpc" "base_vpc" {
  cidr_block           = var.base_cidr_block
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "vpc"
  }
}

module "igw_network" {
  source                     = "./modules/subnets"
  vpc_id                     = aws_vpc.base_vpc.id
  include_public_route_table = true
}

module "public_subnet_network" {
  source                            = "./modules/subnets"
  name                              = "public-subnet"
  subnets_cidr                      = var.public_subnets_cidr
  vpc_id                            = aws_vpc.base_vpc.id
  subnet_map_public_ip_on_launch    = true
  availability_zones                = var.availability_zones
  include_private_route_table       = true
  map_subnet_to_public_route_tables = module.igw_network.public_route_tables
}

module "private_network" {
  source                             = "./modules/subnets"
  name                               = "rds"
  subnets_cidr                       = var.private_subnets_cidr
  vpc_id                             = aws_vpc.base_vpc.id
  availability_zones                 = var.availability_zones
  map_subnet_to_private_route_tables = module.public_subnet_network.private_route_tables
}

module "loggings" {
  source = "./modules/loggings"
  loggings = [
    {
      name              = "vpn"
      group_name        = "/vpc/vpn"
      retention_in_days = 1
      stream_name       = "log-vpn"

    }
  ]
}

module "security_groups" {
  source = "./modules/security_groups"
  security_groups = [
    {
      name        = "rds"
      description = ""
      vpc_id      = aws_vpc.base_vpc.id
      ingress_rules = [
        {
          from_port   = 5432
          to_port     = 5432
          protocol    = "tcp"
          cidr_blocks = ["0.0.0.0/0"]
        }
      ]
      egress_rules = [
        {
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
        }
      ]
    },
    {
      name        = "vpn"
      description = ""
      vpc_id      = aws_vpc.base_vpc.id
      ingress_rules = [
        {
          from_port   = 443
          to_port     = 443
          protocol    = "udp"
          cidr_blocks = ["0.0.0.0/0"]
        }
      ]
      egress_rules = [
        {
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
        }
      ]
    }
  ]
}
