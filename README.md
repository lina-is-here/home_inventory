Home Inventory
==============

Simple app to track items at home and use (eat) them before the expiry date.


Configuration
-------------
The app expects the following variables in the `.env` file in `./home_inventory` directory.
The variables are:
* `HI_SECRET_KEY` – A secret key for a particular Django installation. This is used to provide cryptographic signing, 
  and should be set to a unique, unpredictable value. 
  See more in the [Django docs](https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-SECRET_KEY). 
  One of the possible ways to generate it is by running
  `$python3 -c 'import secrets; print(secrets.token_hex(100))'`.
* `POSTGRES_DB` – name of the database.
* `POSTGRES_USER` – user with superuser power in PostgreSQL.
* `POSTGRES_PASSWORD` – superuser password for PostgreSQL. 
  [More on the `POSTRGRES_` variables](https://hub.docker.com/_/postgres).

See `home_inventory/.env_example` for the example.


Certificates
------------
Docker-compose expects certificates in order to run the app using HTTPS.
This is required for the barcode reading feature to work on mobile devices.

From the root of the project:
```shell
# create the directory for certificates
$ mkdir certs
$ cd certs

# create certificates
$ openssl req \
       -newkey rsa:2048 -nodes -keyout domain.key \
       -x509 -days 365 -out domain.crt

```

Running
-------
`$ docker-compose up`

In case of changes, run
`$ docker-compose up --build`
to rebuild the images.