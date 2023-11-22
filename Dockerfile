FROM python:alpine

RUN sed -i 's|https://dl-cdn.alpinelinux.org|http://mirrors.tuna.tsinghua.edu.cn|g' /etc/apk/repositories

RUN apt-get update \
    && apt-get install -y gcc musl-dev libffi-dev libssl-dev ca-certificates cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apk add --no-cache --virtual .build-app curl

RUN pip config set global.index-url 'https://mirrors.sustech.edu.cn/pypi/web/simple'

RUN curl -sSL https://pdm-project.org/install-pdm.py | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN pdm config pypi.url 'https://mirrors.sustech.edu.cn/pypi/web/simple'

WORKDIR /srv

COPY ./utils ./utils

COPY ./pyproject.toml ./pdm.lock ./miuitask.py ./

RUN pdm install --prod

RUN { crontab -l; printf '%s\t%s\t%s\t%s\t%s\t%s\n' '0' '4' '*' '*' '*' '/usr/bin/env pdm run python /srv/miuitask.py'; } | crontab -

RUN apk del .build-app

VOLUME ["./data", "/srv/data"]

CMD ["/usr/sbin/crond", "-f"]
