#! /usr/bin/sh

# check for root privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# run docker-compose.dev.yml and add any additional arguments
docker compose -f docker-compose.dev.yml up "$@"