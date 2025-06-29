FROM python:3.13.2-slim-bullseye

RUN mkdir /opt/app
WORKDIR /opt/app

# Install build dependencies and libpq
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "main.py"]
