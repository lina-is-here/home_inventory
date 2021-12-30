FROM python:3.9-slim

ENV DJANGO_SETTINGS_MODULE=home_inventory.settings_production

COPY . .

RUN python -m pip install --upgrade pip && \
    apt-get update && apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "/entrypoint.sh"]
