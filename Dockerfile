FROM python:3.6.1-alpine
ADD . /opt/consync
WORKDIR /opt/consync
RUN pip install /opt/consync
VOLUME /data
ENTRYPOINT ["/usr/local/bin/consync"]
