FROM python:3.9-slim

COPY . .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["pytest", "tests"]
