FROM tomcat:7.0-jre8-alpine

ENV JAVA_OPTS "${JAVA_OPTS} -Xms512m -Xmx1024m -XX:+UseParallelGC -server "

RUN rm -rf /usr/local/tomcat/webapps/* && \
    mkdir -p /var/www/content/searchIndex \
    mkdir -p /var/www/content/site_files

COPY ./distr/site/ROOT.war /usr/local/tomcat/webapps/

EXPOSE 8080

CMD ["catalina.sh", "run"]