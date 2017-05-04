FROM python:3.6.1-alpine
RUN apk add --update nodejs
RUN npm install -g droppy
ADD . /opt/consync
WORKDIR /opt/consync
RUN pip install /opt/consync
VOLUME /data
ENTRYPOINT ["/opt/consync/starter.sh"]
