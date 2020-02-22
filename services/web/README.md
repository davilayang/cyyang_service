
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
