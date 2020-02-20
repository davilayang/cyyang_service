FROM python:3.6.9-alpine

WORKDIR /usr/src

# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev
# apk add gcc g++ make python3-dev

RUN apk update

COPY ./requirements.txt .
RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

COPY . . 