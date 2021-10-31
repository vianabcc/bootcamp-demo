# API Bootcamp Example

## Setup project

### Create a virtualenv and activate it

Inside root project directory, run:

```sh
  ❯ python3 -m virtualenv venv
  ❯ source ./venv/bin/activate
``` 

### Install dependencies

```sh
  ❯ pip install -r requirements.txt
``` 

### Run project

```sh
  ❯ uvicorn app:api:app --reload
``` 
