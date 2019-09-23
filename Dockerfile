FROM ubuntu:19.04

LABEL maintainer="lvc0107@protonmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    apt-get install libpq-dev -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
