FROM python:latest
EXPOSE 5000
RUN pip install flask uuid flask_cors requests
COPY players.py /opt/players.py
WORKDIR /opt

CMD python3 /opt/players.py

