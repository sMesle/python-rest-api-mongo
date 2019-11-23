# python-rest-api-mongo
Python CRUD rest api with flask and mongodb

## Project setup

### MongoDB

MongoDB Setup
```console
smesle@smesle-pc:~$ docker run -d -p 27017-27019:27017-27019 --name mongodb mongo
```
Go in the mongodb shell
```console
smesle@smesle-pc:~$ docker exec -it mongodb mongo
```

```console
mongodb@shell$ use actors
```
