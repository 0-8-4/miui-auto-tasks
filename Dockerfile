FROM python:3.9-alpine

COPY ./utils /srv/utils/

COPY ./requirements.txt /tmp

COPY ./config.env ./miuitask.py /srv

COPY crontab /var/spool/cron/crontabs/root

RUN pip install -i https://mirrors.bfsu.edu.cn/pypi/web/simple  -r /tmp/requirements.txt && \
    rm -rf /tmp/*

WORKDIR /srv

CMD ["/usr/sbin/crond", "-f"]