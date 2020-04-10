#!/bin/sh
# make sure pg is ready to accept connections
until ./pg_isready
do
  echo "Waiting for postgres"
  sleep 1;
done

# Now able to connect to postgres