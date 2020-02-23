
# `Flask` Servcice Structure

## Tree Map

```bash
.
├── CHANGELOG.md
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── README.md
├── config
│   ├── ...
│   └── ...
├── k8s
├── mypy.ini
├── app
│   ├── __init__.py
│   ├── api.py
│   └── ...
└── tests
    ├── __init__.py
    └── ...
```

## Folders

### config

### k8s

### app, as the main module

+ `__init__.py`
  + ...
+ `api.py`
  + basic routes and app
+ `routes.py`
  + chart routes
+ `food_reviews`
  + food reviews project data

### `tests`


## Dockerfile

+ build image 
  + `docker image build --tag cyyang-flask .`
+ run container
  + `docker container run -it --rm --publish 8000:5001 cyyang-flask /bin/ash`
  + `docker container run --publish 8000:5001 cyyang-flask`
+ remove image
  + `docker image rm cyyang-flask`

### Usage

> communicate between web and database using _bridge: cyy-network_

1. start database with network
    + `docker container run --name psqldb --rm --network cyy-network -p 5432:5432 cyyang-db`
2. start flask with network
    + `docker container run -it --rm --network cyy-network cyyang-flask /bin/ash`
      + `python manage.py reset_db`

> bind mount for developing

1. start database with network

```bash
docker container run --rm \
  --name psqldb \
  --network cyy-network \
  --publish 5432:5432 \
  cyyang-db
```

2. start flask with network

```bash
docker container run --rm \
  --name flask-dev \
  --network cyy-network \
  --publish 8080:5001 \
  --mount type=bind,source="$(pwd)"/services/web,target=/usr/src \
  cyyang-flask
```
    + `--volume "$(pwd)"/services/web:/usr/src` 

3. exec into flask-dev

```bash
docker exec -it flask-dev /bin/ash
```
