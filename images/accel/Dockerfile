FROM alpine:latest

RUN apk update && apk add varnish

COPY run.sh /
COPY ./etc/* /etc/varnish/

EXPOSE 9000

CMD [ "sh", "/run.sh", "check" ]
ENTRYPOINT [ "sh", "/run.sh" ]
