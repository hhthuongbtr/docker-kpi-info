FROM centos:centos7

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y httpd mod_wsgi \
                   mariadb mariadb-server
                   python-pip python-setuptools \
RUN easy_install supervisor
RUN pip install django

ADD supervisord.conf /etc/supervisord.conf

#CMD mariadb-prepare-db-dir %n
#CMD mysqld_safe --basedir=/usr
#CMD /usr/libexec/mariadb-wait-ready $MAINPID
CMD httpd -DFOREGROUND
