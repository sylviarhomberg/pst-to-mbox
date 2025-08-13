FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    pst-utils \
    libpst4 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py /app/
CMD ["python", "main.py"]
