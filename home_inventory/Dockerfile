FROM python:3.9-slim

ENV DJANGO_SETTINGS_MODULE=home_inventory.settings_production

COPY . .

RUN groupadd -g 1001 uwsgi-group && \
    useradd -u 1001 -g 1001 -s /usr/sbin/nologin uwsgi-user && \
    python -m pip install --upgrade pip && \
    apt-get update && apt-get install -y libpq-dev gcc libpcre3 libpcre3-dev postgresql-client && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "./entrypoint.sh"]
