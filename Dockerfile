FROM python:3.12.0-slim

RUN apt-get update \
    && apt-get install -y gcc musl-dev libffi-dev libssl-dev ca-certificates cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pdm

COPY ./utils /srv/utils/

COPY ./miuitask.py /srv/

COPY pyproject.toml pdm.lock /srv/

WORKDIR /srv

RUN pip install --no-cache-dir urllib3 certifi

RUN pdm install --prod && \
    echo "0   4	*	*	*	python /srv/miuitask.py" > /var/spool/cron/crontabs/root

VOLUME ["./data", "/srv/data"]

CMD ["/usr/sbin/crond", "-f"]
