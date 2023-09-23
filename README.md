# alembic-rds-vpn-terraform

## Local Development
#### Initialisation (DO NOT RUN AGAIN)
- Start docker server for postgres. `docker compose up --build`
- Install package. `pip install -e .[dev,alembic]`
- Initialise alembic structure.
    ```
    alembic init alembic
    alembic -n dev revision --autogenerate -m "init persons table"
    alembic -n dev upgrade head
    ```
#### Maintance
- Start docker server for postgres. `docker compose up --build`
- Install package. `pip install -e .[dev,alembic]`
- Initialise postgres table.
    ```
    alembic -n dev upgrade head
    ```
- Update table.
    ```
    pip install -e .[dev,alembic]
    alembic -n dev revision --autogenerate -m "new feature"
    alembic -n dev upgrade head
    ```

## Cloud Development
#### Initialisation (DO NOT RUN AGAIN)
- Build cloud infrastructure for postgres.
    ```
    git clone https://github.com/OpenVPN/easy-rsa.git
    cd easy-rsa/easyrsa3
    ./easyrsa init-pki
    ./easyrsa build-ca  # add your passphrase
    ./easyrsa build-server-full server nopass
    ./easyrsa build-client-full client1.domain.tld nopass
    mkdir ~/my-vpn-files/
    cp pki/ca.crt ~/my-vpn-files/
    cp pki/issued/server.crt ~/my-vpn-files/
    cp pki/private/server.key ~/my-vpn-files/
    cp pki/issued/client1.domain.tld.crt ~/my-vpn-files
    cp pki/private/client1.domain.tld.key ~/my-vpn-files/
    cd architecture
    terraform init
    terraform apply -auto-approve
    ```
- Download VPN file.
    - AWS Console > VPN Endpoint > download client configuration > `downloaded-client-config.ovpn`
    - In downloaded-client-config.ovpn, above `reneg-sec 0` and below `</ca>`, insert followings...
        ```
        <cert>
        # ...from client1.domain.tld.cert wrapped (Don't include this line)
        -----BEGIN CERTIFICATE-----
        xxxxxx
        -----END CERTIFICATE-----
        </cert>

        <key>
        # ...from client1.domain.tld.key wrapped (Don't include this line)
        -----BEGIN PRIVATE KEY-----
        xxxxxx
        -----END PRIVATE KEY-----
        </key>
        ```
    - Import `downloaded-client-config.ovpn` to openvpn client.
- Install package. `pip install -e .[dev,alembic]`
- Initialise alembic structure.
    ```
    export AWS_ACCESS_KEY_ID=
    export AWS_SECRET_ACCESS_KEY=
    export AWS_DEFAULT_REGION=
    alembic init alembic
    alembic -n cloud revision --autogenerate -m "init persons table"
    alembic -n cloud upgrade head
    ```

#### Maintance
- Install package. `pip install -e .[dev,alembic]`
- Initialise postgres table.
    ```
    export AWS_ACCESS_KEY_ID=
    export AWS_SECRET_ACCESS_KEY=
    export AWS_DEFAULT_REGION=
    alembic -n cloud upgrade head
    ```
- Update table.
    ```
    export AWS_ACCESS_KEY_ID=
    export AWS_SECRET_ACCESS_KEY=
    export AWS_DEFAULT_REGION=
    pip install -e .[dev,alembic]
    alembic -n cloud revision --autogenerate -m "new feature"
    alembic -n cloud upgrade head
