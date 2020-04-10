#!/bin/bash

until [ "`wget -q -O- http://localhost:8080 | grep 'Главная'`" != "" ];
do
  echo "Waiting for site"
  sleep 3
done

echo Tomcat is ready!