#!/bin/bash

echo "Stop all Development Containers"

docker container stop psqldb flaskdev

echo "Development Containers Stopped!"