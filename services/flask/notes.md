
# Flask Backend

## Image/Dockerfile

Build from Dockerfile

```bash
cd /d/AdminData/Documents/cyyang_service
docker image build --tag cyyange-flask .
```
<!-- markdownlint-disable MD034 -->
Start container  
visits the root page at http://localhost:8080/  
or `curl localhost:8080`
<!-- markdownlint-ensable MD034 -->
```bash
docker container run --publish 8080:5001 cyyang-flask
# interactive shell
docker container run -it --rm -p 8080:5001 cyyang-flask /bin/bash
```

Remove images

```bash
docker image rm cyyang-flask
# remove all unneeded
docker image prune
```

## Communicate with `bridge` network

> For the `flask` and `db` containers to talk to each other, they need to be one the same network, which is connected with _bridge network_.  

Create a `bridge` network

```bash
docker network create --driver bridge cyy-network
docker network inspect cyy-network
```

Start the containers by specifying `--network`

```bash
# db
docker container run \
  --rm --network cyy-network \
  --name some-psql -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -v psql-data:/var/lib/postgresql/data postgres:12.0-alpine
# flask
# make sure .env.dev has the correct env, i.e. some-psql:5432
docker container run \
  --rm --network cyy-network \
  --name some-flask --env-file .env.dev \
  cyyang-flask
```

Exec into flask container and populate database

```bash
docker exec -it some-flask /bin/bash
## inside the container
python manage.py reset_db
python manage.py seed_all
```

Exec into database container

```bash
docker exec -it some-psql /bin/bash
## within the container
psql -U user testdb
```

## Development with `docker run`

(or, `sh services/dev.sh`)

Start Containers

```bash
# load .env file at project root
cd /d/AdminData/Documents/cyyang_service/
```

```bash
# start postgresql with persistent volume
docker container run \
  --network cyy-network --name dev-psql \
  --env-file .env.dev \
  -v psql-data:/var/lib/postgresql/data \
  postgres:12.0-alpine
```

```bash
# start flask with bind mount
docker container run --rm \
  --network cyy-network --name dev-flask \
  --publish 8080:5001 --env-file .env.dev \
  --mount type=bind,source="$(pwd)"/services/flask,target=/usr/src \
  cyyang-flask
# --volume "$(pwd)"/services/web:/usr/src
```

Exec into the containers

```bash
# postgres
docker exec -it dev-psql /bin/ash
# flask
docker exec -it dev-flask /bin/bash
```

## References

+ [Gunicorn - WSGI server](https://docs.gunicorn.org/en/stable/)
