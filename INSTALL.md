

# Shorter URL Application
This application contains the APIs for translate long URLs in short URLs.

## Getting Started
#### First make sure you run this code in a virtual environment:

* pip (or conda) package manager are required
`python3 -m venv shorter_venv`
`source shorter_venv/bin/activate`

#### Create DB
1. docker pull postgres
2. docker run --name docker-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
3. docker exec -it docker-postgres /bin/bash
4. su  postgres
5. psql
6. create database shorter_db;

#### Now to get the app running:

1. Create a build `./build.sh`
2. Start the local dev server `./server.sh`
3. Check that the app is running: http://localhost:5000/shorter/healthcheck/
4. For Unit test execute `pytest`
5. For Feature test execute `behave`


## Database

### Applying Changes  
Alembic is in implementation process

###TODO:

* Complete UT for all APIs
* Change SQL DB for some NON-SQL DB
* Dockerize
* Add log
* Test date object properly
