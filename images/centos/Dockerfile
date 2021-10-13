FROM centos:7

ENV GOSU_VERSION 1.11
ENV GPG_KEYS B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN set -ex; \
	yum -y install epel-release; \
	yum -y install glibc-locale-source wget dpkg; \
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /tmp/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
# verify the signature
	export GNUPGHOME="$(mktemp -d)"; \
	( gpg --yes --always-trust --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEYS" || gpg --yes --always-trust --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys "$GPG_KEYS" || gpg --yes --always-trust --keyserver gpg --yes --always-trust --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys "$GPG_KEYS" --recv-keys "$GPG_KEYS" || gpg --yes --always-trust --keyserver pgp.mit.edu --recv-keys "$GPG_KEYS" || gpg --yes --always-trust --keyserver keyserver.pgp.com --recv-keys "$GPG_KEYS" ); \
	gpg --batch --verify /tmp/gosu.asc /usr/bin/gosu; \
	rm -r "$GNUPGHOME" /tmp/gosu.asc; \	
	chmod +x /usr/bin/gosu; \
# verify that the binary works
	gosu nobody true; \
	yum -y remove wget dpkg; \
# russian locale
    localedef -f UTF-8 -i ru_RU ru_RU.UTF-8; \
# ImageMagick & httpd & xorg-x11-server-Xvf
    yum -y --setopt=tsflags=nodocs install ImageMagick httpd which xorg-x11-xauth dbus-x11 xorg-x11-server-Xvfb cifs-utils ca-certificates update-ca-trust; \
    dbus-uuidgen > /var/lib/dbus/machine-id; \
	yum clean all

ENV LANG ru_RU.utf8
ENV DISPLAY localhost:99.0

ADD ./fonts/msttcorefonts.tar.gz /usr/share/fonts/truetype/msttcorefonts/