# Database Service Structure

## Dockerfile

+ build image with Dockerfile
  + `docker image build --tag cyyang-db .`
+ create volume
  + `docker volume create psql-data`
+ run container
  + test connection
    + `docker container run --name some-psql --rm -p 5432:5432 -v psql-data:/var/lib/postgresql/data cyyang-db`
    + `docker container exec --it some-psql /bin/ash `
      + `psql -U user testdb`
  + start database daemon
    + `docker container run --name some-psql --rm -p 5432:5432 -v psql-data:/var/lib/postgresql/data -d cyyang-db`
  + start with `postgres:12.0-alpine`
    + `docker container run --name some-psql --rm -p 5432:5432 -v psql-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=password postgres:12.0-alpine`
    + `docker exec -it some-psql /bin/ash`
      + `psql -U postgres`
+ remove image
  + `docker image rm cyyang-db`


## References

+ https://docs.docker.com/storage/volumes/
+ https://docs.docker.com/storage/bind-mounts/
+ https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile
+ https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside
+ https://docs.docker.com/engine/examples/postgresql_service/