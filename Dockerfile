FROM alpine:3.14

CMD sh -c "while true; do chown 3188:3166 /logs/* /data/*; sleep 5; done;"