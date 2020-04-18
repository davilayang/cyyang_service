# Portfolio Services

## Development Setup

```bash
cd services/
# start all containers
sh dev.sh

# stop all containers
sh stop.sh
```

### Front-End Services

> skip for now, add into project later

### Back-End Services

```bash
# initialize bridge network
docker network create --driver bridge cyy_net
```

#### PostgreSQL Database

```bash
# bulid image with ./db/Dockerfile
docker image build --tag cyyang-db ./db/
```

```bash
# start container with persistent volume, psql-data
docker container run --rm \
  --name psqldb \
  --network cyy-network \
  --publish 5432:5432 \
  --volume psql-data:/var/lib/postgresql/data
  cyyang-db
```

#### Flask Server

```bash
# build image with ./flask/Dockerfile
dokcer image build --tag cyyang-flask ./flask/
```

```bash
# start container with bind mount
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

```bash
```

## Deployment Setup

> deploy as containerized docker services

(write a script to use docker-compose to do this)

## References

+ [Dockerizing Flask with Postgres, Gunicorn, and Nginx](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)
+ [Dockerize a Flask App](https://dev.to/riverfount/dockerize-a-flask-app-17ag)
+ [Setting Up Docker for Windows and WSL to Work Flawlessly](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly)
+ [Deploy React Application to Kubernetes Cluster on Google Cloud Platform](https://hackernoon.com/deploy-a-react-application-to-kubernetes-cluster-on-google-cloud-platform-3idt32ha)
