FROM python:3.9-slim

COPY . .

RUN apt-get update && apt-get install -y libpq-dev gcc libpcre3 libpcre3-dev && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["pytest", "tests"]
