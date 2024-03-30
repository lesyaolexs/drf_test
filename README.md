# drf_test

## Requirements
- docker
- docker-compose

## Run web service
Execute command:
```bash
docker-compose up web
```
Documentation and playground:
http://0.0.0.0:8000/docs/

The API endpoints will be available at **127.0.0.1:8000**.

Example curl:
```bash

curl http://127.0.0.1:8000/app/users/ -H 'Authorization: Bearer ${AUTH_STATIC_TOKEN}'
```
## Run test
```bash
make test
```
