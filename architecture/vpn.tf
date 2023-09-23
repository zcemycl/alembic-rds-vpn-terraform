resource "aws_acm_certificate" "server_vpn_cert" {
  certificate_body  = file(var.server_crt_path)
  private_key       = file(var.server_key_path)
  certificate_chain = file(var.ca_cert_path)
}

resource "aws_acm_certificate" "client_vpn_cert" {
  certificate_body  = file(var.client_crt_path)
  private_key       = file(var.client_key_path)
  certificate_chain = file(var.ca_cert_path)
}

resource "aws_ec2_client_vpn_endpoint" "my_client_vpn" {
  description            = "My client vpn"
  server_certificate_arn = aws_acm_certificate.server_vpn_cert.arn
  client_cidr_block      = var.vpn_cidr_block
  vpc_id                 = aws_vpc.base_vpc.id

  security_group_ids = [module.security_groups.security_groups["vpn"].id]
  split_tunnel       = true

  dns_servers = [
    var.vpc_r53_resolver_ip
  ]

  # Client authentication
  authentication_options {
    type                       = "certificate-authentication"
    root_certificate_chain_arn = aws_acm_certificate.client_vpn_cert.arn
  }

  connection_log_options {
    enabled               = true
    cloudwatch_log_group  = module.loggings.log_groups["vpn"].name
    cloudwatch_log_stream = module.loggings.log_streams["vpn"].name
  }

  depends_on = [
    aws_acm_certificate.server_vpn_cert,
    aws_acm_certificate.client_vpn_cert
  ]
}

resource "aws_ec2_client_vpn_network_association" "client_vpn_association_private" {
  count                  = length(var.private_subnets_cidr)
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.my_client_vpn.id
  subnet_id              = module.private_network.subnet_ids[count.index]

  depends_on = [
    module.private_network
  ]
}

resource "aws_ec2_client_vpn_authorization_rule" "authorization_rule" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.my_client_vpn.id

  target_network_cidr  = var.vpc_cidr
  authorize_all_groups = true
}

resource "aws_ec2_client_vpn_authorization_rule" "authorization_rule_private" {
  for_each               = toset(var.private_subnets_cidr)
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.my_client_vpn.id
  target_network_cidr    = each.value
  authorize_all_groups   = true
}
