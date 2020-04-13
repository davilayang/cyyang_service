# Portfolio Services

## Development Setup

start local containers with script:

```bash
sh dev.script
```

### Front-End

> skip for now, add into project later

### Back-End

```bash
# on this bridge network
docker network create --driver bridge cyy_net
```

#### PostgreSQL Database

```bash
docker container run --rm \
  --name psqldb \
  --network cyy-network \
  --publish 5432:5432 \
  --volume psql-data:/var/lib/postgresql/data
  cyyang-db
```

#### Flask Server

```bash
cd /d/AdminData/Documents/cyyang_service/
docker container run --rm \
  --name flask-dev \
  --network cyy-etwork \
  --publish 8080:5001 \
  --mount type=bind,source="$(pwd)"/services/web,target=/usr/src \
  cyyang-flask
```

#### Nginx Server


## Deployment Setup

> deploy as containerized docker services