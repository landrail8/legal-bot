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

# use -u for getting printed data from print() func
CMD ["python", "-u", "eaglebot.py"]