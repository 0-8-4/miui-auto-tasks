FROM python:alpine

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

RUN pip install --no-cache-dir pdm

WORKDIR /srv

COPY ./utils ./utils

COPY ./pyproject.toml ./pdm.lock ./miuitask.py ./

RUN pdm install --prod

VOLUME ["./data", "/srv/data"]

VOLUME ["./logs", "/srv/logs"]

CMD ["pdm", "run", "python", "miuitask.py"]
