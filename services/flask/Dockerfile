# Flask Dockerfile for container run
FROM python:3.6.10-slim

# prepara for installations
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# set python not writing .pyc and not buffering tdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set working directory
WORKDIR /usr/src

# install python dependencies,
# with docker cache to avoid incessary re-install
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy other files
COPY . .

# set flask Enviroment Variables
ENV FLASK_APP="./app/api.py"
ENV FLASK_RUN_PORT="5001"

# start flask development server
CMD ["flask", "run", "--host=0.0.0.0"]


# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# goal: container run can start a working flask dev server