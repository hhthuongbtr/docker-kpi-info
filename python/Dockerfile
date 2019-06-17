FROM python:3.7.3-stretch
COPY requirements.txt /
RUN pip install -r /requirements.txt
WORKDIR /usr/share/nginx/html
CMD ["uwsgi", "--ini", "/usr/share/nginx/html/kpi_info_uwsgi.ini"]
