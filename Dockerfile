FROM python:3.13.7-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

# Build deps and libpq (for psycopg2); minimal install
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) remove build tools to slim the final image
# RUN apt-get purge -y --auto-remove build-essential && rm -rf /var/lib/apt/lists/*

# App code
COPY . .

# Run as non-root
RUN useradd -m -r -d /opt/app -s /usr/sbin/nologin app && chown -R app:app /opt/app
USER app

CMD ["python", "-u", "main.py"]
