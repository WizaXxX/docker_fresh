#!/bin/bash

set -e

if [ "$1" = './postgres' ]; then
    if [ ! -s "$PGDATA/PG_VERSION" ]; then
        chown -R postgres:postgres "$PGDATA"
        gosu postgres ./initdb
        echo "synchronous_commit = off" >> "$PGDATA/postgresql.conf"
        echo "unix_socket_directories = '/tmp,$PGSOCKET'" >> "$PGDATA/postgresql.conf"
    fi
    chown postgres $PGSOCKET
    exec gosu postgres ./postgres
fi

exec "$@"