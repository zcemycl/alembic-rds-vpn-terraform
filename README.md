# alembic-rds-vpn-terraform

### Setup
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


### Cloud database migration
```
```
