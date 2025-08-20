#!/bin/bash
echo "Removing docker-compose.yaml to ensure single-container deployment..."
rm -f /var/app/staging/docker-compose.yaml

echo "Moving Dockerfile to root for single-container deployment..."
cp /var/app/staging/deployment/Dockerfile /var/app/staging/Dockerfile
