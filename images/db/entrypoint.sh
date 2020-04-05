#!/bin/bash

set -e

chown -R postgres:postgres "$PGDATA"

if [ -z "$(ls -A "$PGDATA")" ]; then
    gosu postgres ./initdb
    echo "synchronous_commit = off" >> $PGDATA/postgresql.conf
fi

command=$@
exec gosu postgres $command