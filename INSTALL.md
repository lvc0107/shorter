
## Getting Started
#### First make sure you run this code in a virtual environment:

* pip (or conda) package manager is required
1. `python3 -m venv shorter_venv`
2. `source shorter_venv/bin/activate`

#### Create DB
1. `docker pull postgres`
2. `docker run --name docker-postgres-shorter -e POSTGRES_PASSWORD=mysecretpassword -d postgres`
3. `docker exec -it docker-postgres /bin/bash`
4. `su postgres`
5. `psql`
6. create database shorter_db;

#### Now to get the app running:

1. Create a build `./build.sh`
2. Start the local dev server `./server.sh`
3. Check that the app is running: http://localhost:5000/shorter/healthcheck/
4. For Unit test execute `pytest`
5. For Feature test execute `behave`

### Docker

1. `docker build -t shorter_app:latest .`
2. `docker rm shorter_app_container; docker run -p 5000:5000 --name shorter_app_container shorter_app`


### Some aditional commands
1. `docker stop shorter_app_container`
2. `docker rm shorter_app_container`
3. `docker exec -it shorter_app_container sh`
4. `curl -X GET http://localhost:5000/shorter/healthcheck/`


## Database

### Applying Changes  
Alembic is in implementation process

###TODO:

* Complete UT for all APIs
* Change SQL DB for some NON-SQL DB
* Qubernete
* Add log
* Test date object properly
* Add OIDC

