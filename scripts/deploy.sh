#!/bin/bash
set -euo pipefail

# Required environment variables
: "${DOMAIN:?DOMAIN variable not set}"
: "${STACK_NAME:?STACK_NAME variable not set}"
: "${TAG:?TAG variable not set}"

# Build the images
echo "Building images with tag: $TAG"
docker compose -f docker-compose.yml build

# Deploy the stack to Swarm
echo "Deploying stack: $STACK_NAME"
docker stack deploy -c docker-compose.yml $STACK_NAME

echo "Deployment of stack $STACK_NAME completed successfully!"