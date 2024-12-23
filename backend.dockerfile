FROM python:3.12-slim-bullseye

LABEL maintainer="Jonathan Bereyziat <contact@bereyziat.dev>"

COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app

ENV PYTHONPATH=/app
# Set the working directory
WORKDIR /app

ARG TAG

RUN bash -c "if [ $TAG == 'dev' ]; then uv export --no-hashes > requirements.txt; else uv export --no-hashes --no-dev > requirements.txt; fi"
RUN uv pip install --system -r requirements.txt

EXPOSE 80

CMD ["/start.sh"]