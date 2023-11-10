FROM python:3.11.6-alpine

COPY ./utils /srv/utils/

COPY ./requirements.txt /tmp

COPY ./config.template.yaml ./miuitask.py ./main.py /srv/

COPY /srv/config.template.yaml /srv/config.yaml
RUN pip install --no-cache-dir -i https://mirrors.bfsu.edu.cn/pypi/web/simple -r /tmp/requirements.txt && \
    rm -rf /tmp/* 

WORKDIR /srv

CMD ["python", "main.py"]
