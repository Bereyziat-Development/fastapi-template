#! /usr/bin/env sh

# Exit in case of error
# set -e

# DOMAIN=${DOMAIN?Variable not set} \
# TRAEFIK_TAG=${TRAEFIK_TAG?Variable not set} \
# STACK_NAME=${STACK_NAME?Variable not set} \
# TAG=${TAG?Variable not set} \
# docker compose \
# -f docker-compose.yml \
# config | tail -n +2 > docker-stack.yml

# docker-auto-labels docker-stack.yml

# docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"


#!/bin/bash
set -euo pipefail

# Required environment variables
: "${DOMAIN:?DOMAIN variable not set}"
: "${TRAEFIK_TAG:?TRAEFIK_TAG variable not set}"
: "${STACK_NAME:?STACK_NAME variable not set}"
: "${TAG:?TAG variable not set}"

# Build the images
echo "Building images with tag: $TAG"
docker compose -f docker-compose.yml build

# Generate the Docker stack configuration
echo "Generating stack file for deployment"
docker compose -f docker-compose.yml config | tail -n +2 > docker-stack.yml

# Deploy the stack to Swarm
echo "Deploying stack: $STACK_NAME"
docker stack deploy -c docker-stack.yml --with-registry-auth "$STACK_NAME"

echo "Deployment of stack $STACK_NAME completed successfully!"