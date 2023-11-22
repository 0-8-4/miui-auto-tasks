FROM python:alpine

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

RUN apk add --no-cache --virtual .build-app curl

RUN curl -sSL https://pdm-project.org/install-pdm.py | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /srv

COPY ./utils ./utils

COPY ./pyproject.toml ./miuitask.py ./

RUN pdm install --prod

RUN { crontab -l; printf '%s\t%s\t%s\t%s\t%s\t%s\n' '0' '4' '*' '*' '*' '/usr/bin/env pdm run python /srv/miuitask.py'; } | crontab -

RUN apk del .build-app

VOLUME ["./data", "/srv/data"]

CMD ["/usr/sbin/crond", "-f"]
