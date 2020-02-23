
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
  + `docker container run -it --rm --publish 8080:5001 cyyang-flask /bin/ash`
  + `docker container run --publish 8080:5001 cyyang-flask`
+ remove image
  + `docker image rm cyyang-flask`

### Usage

#### Containers in Single Network

_Bridge network_  

> postgresql://\<user>:\<password>@psqldb:5432/\<database>

```bash
# create network
docker network create --driver bridge cyy_net
docker network inspect cyy_net

# start database container
docker run --name psqldb --rm --network cyy_net -p 5432:5432 cyyang-db

# start web container to test
docker run -it --rm --network cyy_net cyyang-flask /bin/ash
python manage.py reset_db

# exec database to check
docker exec -it psqldb /bin/ash
## inside flask-dev container
psql -U user testdb

```

#### Development with `Flask` and `Posgresql`

_Start Containers_

> http://localhost:8080

```bash
# start postgresql, with custom image
docker container run --rm \
  --name psqldb \
  --network cyy-network \
  --publish 5432:5432 \
  --volume psql-data:/var/lib/postgresql/data
  cyyang-db
```

```bash
# start flask, with custom image
cd /d/AdminData/Documents/cyyang_service/
docker container run --rm \
  --name flask-dev \
  --network cyy-network \
  --publish 8080:5001 \
  --mount type=bind,source="$(pwd)"/services/web,target=/usr/src \
  cyyang-flask
# --volume "$(pwd)"/services/web:/usr/src
```

_Exec into the containers_

```bash
# postgresql
docker exec -it psqldb /bin/ash

# flask
docker exec -it flask-dev /bin/ash
```