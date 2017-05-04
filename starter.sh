#!/bin/sh
CONSUL_SERVER=${CONSUL_SERVER:-localhost:8500}
droppy start -f /data -c /opt/consync/ &
consync --url $CONSUL_SERVER /data conf
consync --serve --url $CONSUL_SERVER /data conf
