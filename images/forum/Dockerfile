FROM tomcat:7.0-jre8-alpine

ENV JAVA_OPTS "${JAVA_OPTS} -Xms256m -Xmx512m -XX:+UseParallelGC -server"

RUN rm -rf /usr/local/tomcat/webapps/* && \
    mkdir -p /var/www/forum/{mess_files,logo} 

COPY ./distr/forum/ROOT.war /usr/local/tomcat/webapps/

EXPOSE 8080

CMD ["bin/catalina.sh", "run"]