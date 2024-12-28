# FastAPI Backend template

Hey! Ever wanted to get a backend all set in a couple of minutes? Well you are in the right place! 

Using FastAPI and based on [fullstack example project of Tiangolo](https://github.com/tiangolo/full-stack-fastapi-postgresql), this templates allows you to focus on your features with an organized and highly opinionated structure.

Here is what you will be able to find out the box here:

- 🚀 OAuth2.0: Authentication by JWT with access Token and refresh Token
- 🥸 SSO: pre-configured auth with Facebook, Github and Google
- 📧 Email service: delegated email service using SMTP
- 📜 MJML: email templating
- 💽 PostgreSQL/SQLAlchemy: ORM managed database
- 🏁 Alembic: database migration
- 🗂️ File storage: file management on local disk
- 👾 UV: Rust based python package manager
- ✍️ CRUD: easy to setup and to replicate
- 🤖 Pytest: unit tests
- 🐳 Docker stack for development and deployment

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Deployment

This template provides with an out of the box Dockerized deployment on a VPS-like linux server using Traefik as a proxy. Simply update the env vars to match your project and follow the step-by-step [Deployment Documentation](./DEPLOY.md).

## Local development

1. Create a `.env` file.

2. Copy the content from the `env-example` file into your `.env` file.

3. Uncomment the variables to activate the services relevant to your project (e.g., email, file management, SSO credentials).

4. For security, generate random strings for secret keys and add your SSO credentials (Facebook, GitHub, Google) if you plan to use SSO in your project.

5. Once the `.env` file is configured, start the stack with Docker Compose:

    ```bash
    docker compose up -d
    ```

    **Note**: The first time you start your stack, it might take a bit of time to download all the docker images. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

    To check the logs, run:

    ```bash
    docker compose logs
    ```

    To check the logs of a specific service, add the name of the service, e.g.:

    ```bash
    docker compose logs backend
    ```

6. Now you can open your browser and interact with these URLs:

    REST API entry point: http://localhost/api/

    Automatic interactive documentation with Swagger UI: http://localhost/docs

    PGAdmin, PostgreSQL admin platform: http://localhost:5050


### Package management with uv

By default, the dependencies are managed with [uv](https://docs.astral.sh/uv/). You can install uv using pip or with their standalone installer:

```Bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

From the root folder of the project, install all the dependencies with:

```Bash
uv sync
```

That's it, ou are all set!

If you are using VSCode you can simply open the root of the project using the `code` command:
```Bash
code .
```

The python virtual environment should be selected automatically in VSCode. If not, you can specify the path to your interpreter in the `.venv` folder created by the `uv sync` command.

### How to use the template?

Modify or add SQLAlchemy models in `./app/models/`, Pydantic schemas in `./app/schemas/`, API endpoints in `./app/api/`, CRUD (Create, Read, Update, Delete) utils in `./app/crud/`. The easiest might be to copy existing ones (models, endpoints, and CRUD utils) and update them to your needs. Don't forget to run a migration using alembic if you change the models.

### Docker Compose files

The main `docker-compose.yml` file is tailored for development, automatically used by `docker compose`. It enables features like source code mounting and hot-reload via the `start-reload.sh` script but does not include the Traefik service.  

For deployment, the `docker-compose.prod.yml` file is used, invoked by the `deploy.sh` script. Both Compose files rely on the `.env` file to inject environment variables into the containers.

## Testing

### Test during development

To test the backend during development on your local machine, make sure your docker stack is running:

```bash
docker compose up -d
```

Then proceed with running the test.sh script
```Bash
sh ./scripts/test.sh
```

### Test Coverage

Because the test scripts forward arguments to `pytest`, for example:
- ` --cov=app --cov-report=html` to enable test coverage HTML report generation
- `-x` to stop the tests at the fist failing test, which can be useful for debugging.
- `-k "test_api_users"` to run test that are matching the provided string, this can come in handy to isolate a given test or a group of tests.

To run the local tests with coverage HTML reports:

```Bash
sh ./scripts/test.sh --cov=app --cov-report=html
```

### Continuous testing

All tests specified in the `./app/tests` directory are automatically running when pushing or opening a PR to `dev` or `main` branch. You can of course add or modify the GitHub actions in `./.github/workflows` directory according to your needs.

## Migration

During local development, your app directory is mounted as a volume inside the container. This setup allows you to run `alembic` commands directly inside the container, and the migration files will be saved in your app directory. This makes it easy to track them in your Git repository.

### Steps for Database Migration

1. **Generate a Revision**  
   Whenever you make changes to your models (e.g., adding a column), you need to create a new migration revision. Simply run:  
   ```Bash
   sh ./scripts/new-revision.sh -m "Description of your revision"
   ```
   This command generates a migration script in the `./alembic/versions` directory based on your changes. **Don't forget about double checking any migration scripts before applying them.**

2.	**Apply the Migration**
    After creating the revision, apply the changes to the database by running:
    ```Bash
    sh ./scripts/migrate.sh
    ```
    This will update your database schema to match the changes in your models.


**IMPORTANT:** If you created a new model in `./app/models/`, make sure to import it in `./app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

**IMPORTANT:** Remember to add and commit to the git repository the files generated in the alembic directory.

If you don't want to use migrations at all, uncomment the following line in the file `./app/db/init_db.py`:

```python
Base.metadata.create_all(bind=engine)
```

and comment the following line from the `prestart.sh` script:

```Bash
alembic upgrade head
```

If you want to start your migration history from scratch, you can remove all the revision files (`.py` Python files) in `./alembic/versions/`. And then create an initial migration as described above.

## Emails

This templates propose an emails configuration that relies on connecting to your SMTP server. For example you can easily connect your Gmail account with env variables or your custom domain email server. This is a good solution for personal project and staring project but it is highly encourage for scalability and security reasons to transition to a dedicated external service like Sendgrid or any valid alternatives for your production builds.

## File storage/management

This template implement local storage of files. This means that the files like profile pictures, documents or other files you decide to implement in your future project will be stored on the local disc of the running server. Those files are persisted using docker volume. Although its a great method to store files for a small project or during development to avoid setting up any extra configuration, it is highly encourage to replace this by a dedicated S3 object storage for your production builds.

# Roadmap (contribution are welcome):
- [⏳ In progress] Add GitHub actions (run test, listing on push etc)
- [⏳ In progress] S3 simplified connection
- [🔮 Planned] Add a monitoring tool as part of the stack (Prometeus for metrics and Signal for instrumentation ?)
- [🔮 Planned] Connection to an email service like SendGrid or Resend
- [💭 To be considered] Update to utilize Async technology (for endpoints that can benefit from it) https://medium.com/@neverwalkaloner/fastapi-with-async-sqlalchemy-celery-and-websockets-1b40cd9528da#:~:text=Starting%20from%20version%201.4%20SQLAlchemy,let's%20start%20with%20database%20connection. https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- [💭 To be considered] Migration to psycopg v3 could be considered in a future version of the template

## Notes from the author

### ⛔️ Warning about scalability

This template is optimized for deployment on a single VPS or server, providing an easy-to-use solution for small to mid-size projects. The `docker-compose.prod.yml` file offers a comprehensive development setup (including DB, file storage, pgAdmin, etc.) that works well for testing or small-scale deployments. However, it is not optimized for Kubernetes or large-scale production environments out of the box. While it remains production-ready and ideal for simple, manageable structures, it may not scale efficiently for larger or more complex systems.

### License and commercial use

This template is Open-Sourced under the MIT license. This basically means that all contributions are welcome and encouraged. You can use this template or fork it for your personal and commercial use 🥳

If you have questions or encounter any difficulty while using this repo do not hesitate to use the GitHub Discussions channel.

If you need help on your project or look for a commercial collaboration please reach out to my team by email [contact@bereyziat.dev](mailto:contact@bereyziat.dev) or check my [website: bereyziat.dev](https://bereyziat.dev)
