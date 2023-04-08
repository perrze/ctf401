FROM python:latest
EXPOSE 5000
RUN pip install flask pyjwt requests flask_cors
COPY usersAPI.py /opt/usersAPI.py
WORKDIR /opt
CMD python3 /opt/usersAPI.py
