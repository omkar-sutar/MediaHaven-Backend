FROM python:3.9-slim

COPY src /opt/src

COPY requirements.txt /opt/requirements.txt
RUN ["pip","install","-r","/opt/requirements.txt"]
COPY entrypoint.sh /opt/entrypoint.sh
COPY gunicorn.conf.py /opt/gunicorn.conf.py
RUN chmod +x /opt/entrypoint.sh

ENTRYPOINT [ "/opt/entrypoint.sh" ]