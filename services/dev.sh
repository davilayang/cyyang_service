#!/bin/bash

echo "Start PostgreSQL container with bind volume"

docker container run --rm \
  --name psqldb \
  --network cyy-network \
  --publish 5432:5432 \
  --volume psql-data:/var/lib/postgresql/data \
  --detach \
  cyyang-db

echo "Start Flask container"

docker container run --rm \
  --name flaskdev \
  --network cyy-network \
  --publish 8080:5001 \
  --mount type=bind,source=/d/AdminData/Documents/cyyang_service/services/web,target=/usr/src \
  --detach \
  cyyang-flask

echo "Development Containers Started !"