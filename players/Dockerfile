FROM python:3.10.10-alpine3.16

RUN apk update && apk upgrade
RUN apk add git
RUN pip install flask
RUN pip install uuid
RUN pip install re
RUN pip install sqlite3

WORKDIR /home
RUN git clone -b players --single-branch https://github.com/perrze/ctf401.git
WORKDIR /home/ctf401/players

EXPOSE 5000

CMD python players.py

