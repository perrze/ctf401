FROM python:latest
EXPOSE 5000
RUN pip install flask uuid
COPY players.py /opt/players.py
WORKDIR /opt

CMD python3 /opt/players.py

