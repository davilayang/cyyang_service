# Portfolio Services

## Development Setup

```bash
cd services/
# start all containers
sh dev.sh

# stop all containers
sh stop.sh
```

### Front-End

> skip for now, add into project later

### Back-End

```bash
# initialize bridge network
docker network create --driver bridge cyy_net
```

#### PostgreSQL Database

```bash
# bulid image
docker image build --tag cyyang-db ./db/
```

```bash
# start container
docker container run --rm \
  --name psqldb \
  --network cyy-network \
  --publish 5432:5432 \
  --volume psql-data:/var/lib/postgresql/data
  cyyang-db
```

#### Flask Server

```bash
# build image
dokcer image build --tag cyyang-flask ./flask/
```

```bash
# start container`
cd /d/AdminData/Documents/cyyang_service/
docker container run --rm \
  --name flaskdev \
  --network cyy-etwork \
  --publish 8080:5001 \
  --mount type=bind,source="$(pwd)"/services/web,target=/usr/src \
  cyyang-flask
```

#### Nginx Server

```bash
```

## Deployment Setup

> deploy as containerized docker services