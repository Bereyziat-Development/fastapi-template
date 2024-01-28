# FastAPI Backend template

Hey! Ever wanted to get a backend all set in a couple of minutes? Well you are in the right place! 

Using FastAPI and based on [fullstack example project of Tiangolo](https://github.com/tiangolo/full-stack-fastapi-postgresql), this templates allows you to focus on your features with an organized and highly opinionated structure.

Here is what you will be able to find out the box here:

- 🚀 OAuth2.0: authentication with refresh Token
- 🥸 SSO: pre-configured auth with Facebook, Github and Google
- 📧 Email service: delegated email service using SMTP
- 📜 MJML: email templating
- 💽 PostgreSQL/SQLAlchemy: ORM managed database
- 🏁 Alembic: database migration
- 🗂️ File storage: file management on local disk
- ✍️ CRUD: easy to setup and to replicate
- 🤖 Pytest: unit tests
- 🐳 Docker stack for development
- 🌊 DigitalOcean quick deploy (⏳WORK IN PROGRESS⏳)

## Quick deploy option

Digital ocean quick deploy button is already supported for this template but does not manage environment variable auto-creation yet this should be available by February 2024. If you decide to use this repo as a template for your project don't forget to update the link of the button to point to your repo instead of the template.

[![Deploy to Digital Ocean](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/Bereyziat-Development/fastapi-template/tree/main)

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Local development

* Create a .env file

* Copy the content of env-example file to your .env file

* Add/Modify the values to match your project, for example it is highly encouraged to modify the secret keys with randomly generated strings and to add your own SSO credentials for facebook, github and google if you want to use SSO in your project

* Once this done you can start the stack with Docker Compose:

```bash
docker compose up -d
```

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

PGAdmin, PostgreSQL web administration: http://localhost:5050

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker compose logs backend
```

If your Docker is not running in `localhost` (the URLs above wouldn't work) check the sections below on **Development with a custom IP**.

### Poetry

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./` you can install all the dependencies with:

```Bash
poetry install
```

Then you can start a shell session with the new environment with:

```Bash
poetry shell
```

If you are using VSCode you can simply open the root of the project using the `code` command:
```Bash
code .
```

The environment in VSCode should be selected automatically. Otherwise you can specify your interpreter path by copy pasting the path of the freshly created poetry environment.

Modify or add SQLAlchemy models in `./app/models/`, Pydantic schemas in `./app/schemas/`, API endpoints in `./app/api/`, CRUD (Create, Read, Update, Delete) utils in `./app/crud/`. The easiest might be to copy existing ones (models, endpoints, and CRUD utils) and update them to your needs. Don't forget to run a migration using alembic if you do some changes to the models.

### Docker Compose files

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker compose`.

And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume and run the `start-reload.sh` script to enable hot-reload. It is used automatically by `docker compose` to apply overrides on top of `docker-compose.yml`.

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

## Testing

### Tests during development

To test the backend during development on your local machine, make sure your docker stack is running:

```bash
docker compose up -d
```

Then proceed with running the test-local.sh script
```Bash
sh ./scripts/test-local.sh
```

### Test Coverage

Because the test scripts forward arguments to `pytest`, for example:
- ` --cov=app --cov-report=html` to enable test coverage HTML report generation
- `-x` to stop the tests at the fist failing test, which can be useful for debugging.

To run the local tests with coverage HTML reports:

```Bash
sh ./scripts/test-local.sh --cov=app --cov-report=html
```

## Migrations

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have SQL/ORM errors.

**IMPORTANT:** If you created a new model in `./app/models/`, make sure to import it in `./app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

1. After changing a model (for example, adding a column), inside the container, create a revision
```Bash
sh ./scripts/new-revision.sh -m "My new revision message"
```
2. After creating the revision, run the migration in the database (this is what will actually change the database based on the schemas):

```Bash
sh ./scripts/migrate.sh
```

**IMPORTANT:** Remember to add and commit to the git repository the files generated in the alembic directory.

If you don't want to use migrations at all, uncomment the line in the file at `./app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```Bash
alembic upgrade head
```

If you don't want to start with the default models and want to remove/modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./alembic/versions/`. And then create a first migration as described above.

## Emails

This templates propose an emails configuration that relies on connecting to your SMTP server. For example you can easily connect your Gmail account with env variables or your custom domain email server. This is a good solution for personal project and staring project but it is highly encourage for scalability and security reasons to transition to a dedicated external service like Sendgrid or any valid alternatives for your production builds.

## File storage/management

This template implement local storage of files. This means that the files like profile pictures, documents or other files you decide to implement in your future project will be stored on the local disc of the running server. Those files are persisted using docker volume. Although its a great method to store files for a small project or during development to avoid setting up any extra configuration, it is highly encourage to replace this by a dedicated S3 object storage for your production builds.

## Deployment

[⏳ DIGITAL OCEAN: WORK IN PROGRESS ⏳]

### CI/CD

[⏳ GITHUB ACTIONS: WORK IN PROGRESS ⏳]

[⏳ RUNNING TEST: WORK IN PROGRESS ⏳]

## ⛔️ Warning and template usage

This template is designed to be deployed with a Paas service like [Digital Ocean App Platform](https://docs.digitalocean.com/products/app-platform/), or your own Kubernetes/Docker Swarm configuration. 
The `docker-compose.yml` file of this template is designed to provide an all inclusive development experience (db, file storage, pgadmin...).
It could be used as it is in the context of testing or for a small scale deployment but remains poorly scalable and is not suited for production or commercial use.

## Things that will be added (or not depending if we have time 🫣)

### Devops related upgrade:
- Move Database to PSQL on Digital Ocean. DB in production will be separated to allow replication (a docker stack for local development will still be available with postgres 15 -> Latest version available on digital ocean)
- Test and cleanup the gunicorn config files
- Genereate poetry export --without-hashes --format=requirements.txt > requirements.txt on commit or on push
- Add GitHub actions (run test, listing on push etc)
- Add a monitoring tool as part of the stack (Prometeus for metrics and Signal for instrumentation) - See if necessary since we use Digital ocean

### Ideas for later
- Update to utilize Async technology (for endpoints that can benefit from it) https://medium.com/@neverwalkaloner/fastapi-with-async-sqlalchemy-celery-and-websockets-1b40cd9528da#:~:text=Starting%20from%20version%201.4%20SQLAlchemy,let's%20start%20with%20database%20connection. https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Migration to psycopg v3 could be considered in a future version of the template
