#!/bin/bash

cd /d/AdminData/Documents/cyyang_service/

echo "Start PostgreSQL container with persistent volume"

docker container run --rm --detach \
  --network cyy-network \
  --name dev-psql \
  --env-file .env.dev \
  -v psql-data:/var/lib/postgresql/data \
  postgres:12.0-alpine

echo "Start flask container with bind mount"

docker container run --rm --detach \
  --network cyy-network \
  --name dev-flask \
  --publish 8080:5001 \
  --env-file .env.dev \
  --mount type=bind,source="$(pwd)"/services/flask,target=/usr/src \
  cyyang-flask

echo "Development Containers Started !"