set -x

docker compose exec backend alembic revision --autogenerate "$@"
