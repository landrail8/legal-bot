# Deps Stage
FROM python:3.9.6-slim AS builder
WORKDIR /workdir

# copy project
COPY . /workdir

# install dependencies
# RUN pip install --user telebot
RUN pip install -r requirements.txt

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq --no-install-recommends install sqlite3 && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ENTRYPOINT python -c "import sqlite3; print(sqlite3.sqlite_version)"
CMD ["python", "eaglebot.py"]