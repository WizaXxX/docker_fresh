FROM nginx:stable-alpine

ENV HOSTNAME host.1cfresh.dev

ENV SITE_HOST host.1cfresh.dev
ENV BACKEND_HOST host.1cfresh.dev
ENV GATE_HOST host.1cfresh.dev

ENV WORKER_PROCESSES 2

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80 443

ENTRYPOINT ["/bin/sh", "-c", "/entrypoint.sh"]
