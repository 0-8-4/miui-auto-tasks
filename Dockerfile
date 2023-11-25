FROM python:alpine

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

RUN pip install --no-cache-dir pdm

WORKDIR /srv

COPY ./utils ./utils

COPY ./pyproject.toml ./pdm.lock ./miuitask.py ./run.sh ./

RUN pdm install --prod

VOLUME ["/srv/data", "/srv/logs"]

RUN { crontab -l; printf '%s\t%s\t%s\t%s\t%s\t%s\n' '0' '4' '*' '*' '*' '/srv/run.sh'; } | crontab -

CMD ["crond", "-f"]
