FROM python:alpine

RUN apk add gcc

WORKDIR /srv

COPY ./utils ./utils

COPY ./requirements.txt ./miuitask.py ./docker_start.sh ./

RUN pip install -r requirements.txt && \
    echo '0 4 * * * /bin/sh -c "sleep $((RANDOM % 1800 + 1)); cd /srv && python /srv/miuitask.py"' > /var/spool/cron/crontabs/root && \
    chmod +x docker_start.sh

VOLUME ["/srv/data", "/srv/logs"]

CMD ["/srv/docker_start.sh"]
