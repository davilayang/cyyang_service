# Database Service Structure

## Dockerfile

+ build image with Dockerfile
  + `docker image build --tag cyyang-db .`
+ run container
  + `docker container run --name some-psql --rm -p 5432:5432 -v psql-data:/var/lib/postgresql/data -d cyyang-db`
+ remove image
  + `docker image rm cyyang-db`

### Usage

1. start container
    + `docker run --name some-psql --rm -p 5432:5432 cyyang-db`
    + `docker run --name some-psql --rm -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:12.0-alpine`
2. execute command on that container
    + `docker container exec -it some-psql /bin/ash`
      + `psql -U user testdb` , only if the volume has user/testdb
      + `psql -U postgres`


#### Volume for Persistent Data

> volume for persistent data

```bash
# create volume
docker volume create psql-data
```

_copy data form existed unnamed volume_

```bash
# run this from your regular terminal on Windows / MacOS:
docker container run --rm -it -v /:/host alpine

## inside MobyLinux container
chroot /host

# go to volumes
cd /var/lib/docker/volumes
ls -al  # psql-data and <unnamed-volume>

# copy from unamed to named volume
cp -r $(<unnamed-volume>)/* psql-data/*
```

_start with named volume_

```bash
docker run --name some-psql --rm -v psql-data:/var/lib/postgresql/data cyyang-db
docker exec -it some-psql /bin/ash
## inside the some-psql container
psql -U user testdb
```

### Communicate with `bridge` network

> postgresql://postgres:password@psqldb:5432/postgres

```bash
docker network create --driver bridge cyy-network
# docker network inspect cyy-network
docker run --name some-psql --rm --network cyy-network -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:12.0-alpine
docker run --name flask --rm --network cyy-network cyyang-flask
```

## References

+ https://docs.docker.com/storage/volumes/
+ https://docs.docker.com/storage/bind-mounts/
+ https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile
+ https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside
+ https://docs.docker.com/engine/examples/postgresql_service/
+ https://nickjanetakis.com/blog/docker-tip-70-gain-access-to-the-mobylinux-vm-on-windows-or-macos