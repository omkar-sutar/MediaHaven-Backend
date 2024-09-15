FROM --platform=linux/amd64 python:3.9-slim

COPY src /opt/src

COPY requirements.txt /opt/requirements.txt
RUN ["pip","install","-r","/opt/requirements.txt"]
COPY env.sh /opt/env.sh
COPY run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

ENTRYPOINT [ "/opt/run.sh" ]