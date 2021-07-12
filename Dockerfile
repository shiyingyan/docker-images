FROM alpine:3.14

COPY run_main.sh /usr/local/src/
RUN chmod 755 /usr/local/src/run_main.sh
ENTRYPOINT /usr/local/src/run_main.sh
#CMD sh -c "chown 3188:3166 /logs /data; while true; do chown 3188:3166 /logs/* /data/*; sleep 5; done;"
