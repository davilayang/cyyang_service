# Database Backend

[postgres on dockerhub](https://hub.docker.com/_/postgres)  

## Volume for Persistent Data

&nbsp;&nbsp;&nbsp;&nbsp; We want to mount volume of data when a container is created. The main idea is that data are **persistent**, while containers are created/removed based on the workflow.  

Step1: create a volume

```bash
# named as "psql-data"
docker volume create psql-data
```

Step2: populate that empty volume  
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

Step3: check the named volume  

```bash
docker inspect psql-data
```

```bash
docker run --name some-psql --rm -v psql-data:/var/lib/postgresql/data cyyang-db

```

## Image/Dockerfile

&nbsp;&nbsp;&nbsp;&nbsp; Essentially, there is no need to build another image based on that postgres alpine image, since everything has been setup, including `EXPOSE`.  

Start container with posgres alpine

```bash
# detached
docker container run \
  --rm --name some-psql -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -v psql-data:/var/lib/postgresql/data postgres:12.0-alpine
```

Exec into the postgres container

```bash
docker exec -it some-psql /bin/ash
## inside the some-psql container
psql -U user testdb
psql -U postgres
```

### Communicate with `bridge` network

> For the `flask` and `db` containers to talk to each other, they need to be one the same network, which is connected with _bridge network_.  

Create a `bridge` network

```bash
docker network create --driver bridge cyy-network
docker network inspect cyy-network
```

Start the containers by specifying `--network`

```bash
# db
docker container run \
  --rm --network cyy-network \
  --name some-psql -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -v psql-data:/var/lib/postgresql/data postgres:12.0-alpine
# flask
docker container run \
  --rm --network cyy-network --name flask cyyang-flask
```

## References

+ _docker docs_
  + [Use volumes](https://docs.docker.com/storage/volumes/)
  + [Use bind mounts](https://docs.docker.com/storage/bind-mounts/)
  + [Dockerize PostgreSQL](https://docs.docker.com/engine/examples/postgresql_service/)
+ _stackoverflow_
  + [Understanding “VOLUME” instruction in DockerFile](https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile)
  + [Connecting to Postgresql in a docker container from outside](https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside)
+ _others_
  + [Docker Tip #70: Gain Access to the MobyLinux VM on Windows or MacOS](https://nickjanetakis.com/blog/docker-tip-70-gain-access-to-the-mobylinux-vm-on-windows-or-macos)
