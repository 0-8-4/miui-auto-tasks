FROM python:3.9-alpine

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

RUN pip install pdm

COPY ./utils /srv/utils/

COPY ./miuitask.py /srv/

COPY pyproject.toml pdm.lock /srv/

WORKDIR /srv

RUN 

RUN pdm install --prod && \
    echo "0   4	*	*	*	python /srv/miuitask.py" > /var/spool/cron/crontabs/root

VOLUME ["./data", "/srv/data"]

CMD ["/usr/sbin/crond", "-f"]
