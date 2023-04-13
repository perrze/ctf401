FROM python:3.10-alpine

RUN apk update && apk upgrade

RUN pip install flask
RUN pip install uuid

COPY team_programme_bdd.py /opt/team_programme_bdd.py
WORKDIR /opt

EXPOSE 5000

CMD python team_programme_bdd.py