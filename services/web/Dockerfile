# Flask Dockerfile for container run
FROM python:3.6.9-alpine

# set working directory
WORKDIR /usr/src

# prepara for installations
RUN apk update && apk upgrade \
    && apk add python3-dev gcc g++

# set python not writing .pyc and not buffering tdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy other files
COPY . .

# start flask development server
CMD ["flask"]



# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/