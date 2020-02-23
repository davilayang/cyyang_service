# Database Service Structure

## Dockerfile

+ build image with Dockerfile
  + `docker image build --tag cyyang-db .`
+ run container
  + `docker container run --name some-psql --rm -p 5432:5432 -v psql-data:/var/lib/postgresql/data -d cyyang-db`
+ remove image
  + `docker image rm cyyang-db`

### Usage

> test database connection

1. start container
    + `docker container run --name some-psql --rm -p 5432:5432 -v psql-data:/var/lib/postgresql/data cyyang-db`
    + `docker container run --name some-psql --rm -p 5432:5432 -v psql-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=password postgres:12.0-alpine`
2. execute command on that container
    + `docker container exec -it some-psql /bin/ash`
      + `psql -U user testdb` , only if the volume has user/testdb
      + `psql -U postgres`

> volume for persistent data

1. set up _volume_
    + `docker volume create psql-data`

> communicate between web and database using _bridge_

1. set up _bridge_ network
    + `docker network create --driver bridge cyy-network`
    + `docker network inspect cyy-network`
2. start database with the netwrok
    + `docker container run --name psqldb --rm --network cyy-network -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:12.0-alpine`
    + `docker container run --name psqldb --rm --network cyy-network -p 5432:5432 cyyang-db`
3. start web with the network
    + `docker container run --name flask --rm --network cyy-network -p 8080:5001 cyyang-flask`
4. postgres url
    + `postgresql://user:password@psqldb:5432/testdb`
    + `postgresql://postgres:password@psqldb:5432/postgres`

## References

+ https://docs.docker.com/storage/volumes/
+ https://docs.docker.com/storage/bind-mounts/
+ https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile
+ https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside
+ https://docs.docker.com/engine/examples/postgresql_service/