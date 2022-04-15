FROM fresh/centos

ADD ./distr/license-tools /tmp/license-tools
ADD ./distr/*.rpm /tmp/core/

RUN yum -y localinstall /tmp/core/*.rpm; \
    rm -rf /tmp/core; \
    sed -i '/User apache/ s//User usr1cv8/g' /etc/httpd/conf/httpd.conf; \
    sed -i '/Group apache/ s//Group grp1cv8/g' /etc/httpd/conf/httpd.conf; \
    sed -i '/#ServerName www.example.com:80/ s//ServerName localhost/g' /etc/httpd/conf/httpd.conf; \
    yum -y install x11vnc metacity net-tools gdb perl tar git jq; \
    yum -y install https://centos7.iuscommunity.org/ius-release.rpm; \
    yum -y --setopt=tsflags=nodocs install python36u python36u-devel python36u-pip; \
    yum -y install java-1.8.0-openjdk iproute; \
    cert-sync /etc/pki/tls/certs/ca-bundle.crt; \
    oscript /usr/share/oscript/lib/opm/src/cmd/opm.os install deployka; \
    chmod +x /usr/bin/deployka; \
    chmod +x /tmp/license-tools/1ce-installer-cli; /tmp/license-tools/1ce-installer-cli install --ignore-signature-warnings

ENV COREDATA /var/lib/1c/data
ENV CORELOGS /var/log/1c
ENV AGENTBASEDIR /var/lib/1c/agent_data
ENV INFOBASECONNECTIONSTRING ""

VOLUME ["${COREDATA}", "${CORELOGS}", "${AGENTBASEDIR}"]

ADD ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

ADD ./dumper.py /usr/bin/dumper
RUN chmod +x /usr/bin/dumper

ENTRYPOINT ["/entrypoint.sh"]