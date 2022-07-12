FROM fresh/centos

ADD ./entrypoint.sh /

RUN localedef -f UTF-8 -i ru_RU ru_RU.UTF-8 \
    && yum install -y http://repo.postgrespro.ru/pg1c-9.6/keys/postgrespro-1c-9.6.centos.yum-9.6-0.3.noarch.rpm \
    && yum makecache \
    && yum -y --setopt=tsflags=nodocs install postgresql-pro-1c-9.6 --nogpgcheck \
    && chmod +x /entrypoint.sh

EXPOSE 5432

ENV PGDATA /var/lib/1c/pgdata
ENV PGSOCKET /tmp/postgresql/socket

VOLUME ${PGDATA}

WORKDIR /usr/pgsql-9.6/bin
ENTRYPOINT ["/entrypoint.sh"]
CMD ["./postgres"]