# Flask Dockerfile for container run
FROM python:3.6.9-alpine

# set working directory
WORKDIR /usr/src

# prepara for installations
RUN apk update && apk upgrade \
    && apk add --no-cache gcc g++ python3-dev postgresql-dev

# set python not writing .pyc and not buffering tdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install python dependencies,
# with docker cache to avoid incessary re-install
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy other files
COPY . .

# set flask env variables
ENV FLASK_APP="./app/api.py"
ENV FLASK_RUN_PORT=5001
# ENV SQLALCHEMY_TRACK_MODIFICATIONS=False

# start flask development server
CMD ["flask", "run", "--host=0.0.0.0"]


# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# goal: container run can start a working flask dev server