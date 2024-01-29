# Python Fast API
This template provides a boilerplate for getting an API up and running using Docker, Python, and a Postgres database
utilizing the framework [FastAPI](https://fastapi.tiangolo.com/)

## Getting Started
We'll run all the python code through docker to make dependency installation/isolation easier and ease the burden on needing to create a virtual env.

* Run `make dev.setup` - This will set up your local virtual environment and install dev dependencies.
* Run `make up` - This will build and start up the docker container.
* Run `make db.create` - This will create a new database for a new project.
* Run `make db.upgrade` - This will initiate the database and run the migrations
* Run `make db.seed` - This will populate the database with data
* Service will be running at [http://localhost:5000](http://localhost:5000)
* See the API docs at [http://localhost:5000/api](http://localhost:5000/api)
* Pg Admin will be runing at [http://localhost:5050/](http://localhost:5050/) Pgadmin: user: admin, pass: admin. Postgres user: postgres, pass: postgres

## What's included?
- [FastAPI](https://fastapi.tiangolo.com/)
- [Psycopg2](https://www.psycopg.org/docs/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Uvicorn](https://www.uvicorn.org/)
- [PyTest](https://docs.pytest.org/en/6.2.x/)
- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Black](https://black.readthedocs.io/en/stable/index.html)
- [Bumpversion](https://pypi.org/project/bumpversion/)

## Helper commands
This project makes use of a `Makefile` to ease the pain of remembering some common commands and helper utilities within the project.

### Docker helpers
- `make up` - spin up the docker-compose in detached (`-d`) mode.
- `make down` - spin down the docker-compose environment
- `make rebuild` - force a rebuild of the conda container and starts it up
- `make logs` - show the api container logs

### Data helpers
- `make db.upgrade` - runs the alembic migration scripts to update the database with "production" data.
- `make db.upgrade.test` - runs the alembic migration scripts to update the database with test data.
- `make db.downgrade` - completely downgrade the database which will delete all data and delete all tables/indexes/views/etc
- `make db.current` - prints out the current version of the database

### Development environment helpers
- `make dev.setup` - creates and activates a virtual environment and installs all the dependencies into the virtual environment (need to have python 3.9 install locally first)
- `make dev.format` - uses `black` to format the python code
- `make dev.test` - runs the pytest suite and outputs the results

### Documentation helpers
- `make docs` - generates a time stamped `.html` and `openapi.yaml` of the current application in the docs directory
- `make docs.html` - generates only a time stamped `.html` of the current application in the docs directory

## Data
We utilize `alembic` to assist with loading data into the database. Both the alembic scripts and the data for the database are baked into the docker container. They can be run in a deployed environment in order to properly seed the database with data.

For instance, we can use the `Makefile` helpers to populate the local development environment with data:
```bash
# Setup and seed the db with data
$ make db.upgrade
# or
$ make db.upgrade.test

# To clear out the database and start over
$ make db.downgrade
```
## Data Loader
Inside api/helpers is a load_data script that utilizes the methods within the API to load data from a specified json file into the database. This file can be modified to fit the needs of you app.
This data loader script is then connected to the alembic migration script to load data into the app. This script is useful for populating a local test environment or loading data into production environment. This script is also utilized within testing as it loads test data into the test database

## Testing

### Adding new tests

Add tests to the `tests` directory. Test files should be named with `test_` followed by the name of the file it is testing (e.g. `test_main.py` tests `main.py`)

`test_config.py` contains the bootstrapping logic utilized on each test run

### Running Tests

Enter the virtual environment with the command:

`source env/bin/activate`

Then run PyTest using

`make dev.test`

## Building

## Deployment
TODO

## Schema Changes
Schema changes are managed by alembic.
Create a new migration revision with `make new-migration` and edit this file with manual changes.
