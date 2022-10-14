FROM openjdk:8-jre-buster

COPY ./distr/appgate.deb /

RUN dpkg -i /appgate.deb; \
    rm /appgate.deb; \
    echo export PATH=$PATH:/usr/local/openjdk-8/bin > /etc/profile.d/add_java.sh ;\
    chmod +x /etc/profile.d/add_java.sh ;\
    echo export PATH=$PATH:JAVA_HOME=/usr/local/openjdk-8 > /etc/profile.d/add_java_home.sh ;\
    chmod +x /etc/profile.d/add_java_home.sh ;\
    /opt/1C/1cfresh/appgate/setAuth.sh appgate 12345Qwer

EXPOSE 8080 9090

CMD ["/opt/1C/1cfresh/appgate/appgate_wrapper.sh"]