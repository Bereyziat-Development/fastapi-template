#! /usr/bin/env bash

# Exit in case of error
set -e

docker compose exec backend /app/tests-start.sh "$@"
