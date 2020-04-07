FROM java:8-jre

COPY ./distr/appgate.deb /

RUN dpkg -i /appgate.deb; \
    rm /appgate.deb; \
    /opt/1C/1cfresh/appgate/setAuth.sh appgate 12345Qwer

EXPOSE 8080 9090

CMD ["/opt/1C/1cfresh/appgate/appgate_wrapper.sh"]