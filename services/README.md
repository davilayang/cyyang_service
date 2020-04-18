# Portfolio Services

## Development Instruction

```bash
# start all development containers
sh services/dev.sh
# stop all development containers
sh services/stop.sh
```

### FrontEnd

> skip for now, add into project later

### BackEnd

```bash
cd /d/AdminData/Documents/cyyang_service/

# initialize bridge network
docker network create --driver bridge cyy-network
docker network inspect cyy-network
```

#### PostgreSQL Database

```bash
# start container with persistent volume, psql-data
docker container run --rm \
  --network cyy-network \
  --name dev-psql \
  --env-file .env.dev \
  -v psql-data:/var/lib/postgresql/data \
  postgres:12.0-alpine
```

#### Flask Server

```bash
# build image with ./flask/Dockerfile
docker image build --tag cyyang-flask ./services/flask/
```

```bash
# start container with bind mount
docker container run --rm \
  --network cyy-network \
  --name dev-flask \
  --publish 8080:5001 \
  --env-file .env.dev \
  --mount type=bind,source="$(pwd)"/services/flask,target=/usr/src \
  cyyang-flask
```

#### Nginx Server

```bash
# build image with ./nginx/Dockerfile
docker image build --tag cyyang-nginx ./services/nginx/
```

```bash
# start container
docker container run --rm \
  --network cyy-network \
  --name dev-nginx \
  --publish 1337:80 \
  cyyang-nginx
# change the upstream to: server ddv-flask:5001
```

## Deployment Setup

> deploy as containerized docker services

(write a script to use docker-compose to do this)

## References

+ [Dockerizing Flask with Postgres, Gunicorn, and Nginx](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)
+ [Dockerize a Flask App](https://dev.to/riverfount/dockerize-a-flask-app-17ag)
+ [Setting Up Docker for Windows and WSL to Work Flawlessly](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly)
+ [Deploy React Application to Kubernetes Cluster on Google Cloud Platform](https://hackernoon.com/deploy-a-react-application-to-kubernetes-cluster-on-google-cloud-platform-3idt32ha)
