#!/bin/bash

echo "Stop all Development Containers"

docker container stop dev-psql dev-flask

echo "Development Containers Stopped!"