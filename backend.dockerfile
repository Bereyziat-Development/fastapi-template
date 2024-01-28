FROM python:3.11.0

LABEL maintainer="Jonathan Bereyziat <contact@bereyziat.dev>"

COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY . /app
WORKDIR /app/

ENV PYTHONPATH=/app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies in "dev" environment to run tests and lint
RUN bash -c "if [ $ENV_CONFIG == 'dev' ] ; then poetry install --no-root ; else poetry install --no-root --without dev ; fi"

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]

