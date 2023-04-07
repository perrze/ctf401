FROM python:latest
EXPOSE 5000
RUN pip install flask pyjwt requests
COPY usersAPI.py /opt/usersAPI.py
WORKDIR /opt
CMD python3 /opt/usersAPI.py
