# alembic-rds-vpn-terraform

### Local dev Setup
```
alembic init alembic
docker-compose up --build
alembic -n dev revision --autogenerate -m "init persons table"
```

### Local development
```
docker-compose up --build
alembic -n dev upgrade head
```

### Cloud Setup
```
cd architecture
terraform init
terraform apply -auto-approve
```

### Cloud database migration
```
```
