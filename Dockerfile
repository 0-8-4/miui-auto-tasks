FROM python:3.9-alpine

COPY ./utils /srv/utils/

COPY ./requirements.txt /tmp

COPY ./config.env ./miuitask.py /srv/

RUN pip install --no-cache-dir -i https://mirrors.bfsu.edu.cn/pypi/web/simple -r /tmp/requirements.txt && \
    rm -rf /tmp/* && \
    echo "0   4	*	*	*	python /srv/miuitask.py" > /var/spool/cron/crontabs/root

WORKDIR /srv

CMD ["/usr/sbin/crond", "-f"]
