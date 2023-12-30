FROM python:alpine

RUN apk add --no-cache gcc g++ musl-dev python3-dev libffi-dev

RUN pip install --no-cache-dir pdm

WORKDIR /srv

COPY ./utils ./utils

COPY ./pyproject.toml ./pdm.lock ./miuitask.py ./docker_start.sh ./

RUN pdm install --prod && \
    echo "0 4 * * * cd /srv && pdm run /srv/miuitask.py" > /var/spool/cron/crontabs/root && \
    chmod +x docker_start.sh

VOLUME ["/srv/data", "/srv/logs"]

CMD ["/srv/docker_start.sh"]
