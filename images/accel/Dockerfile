FROM alpine:latest

RUN apk update && apk add varnish

WORKDIR /var/lib/varnish
COPY start.sh /

CMD [ "/start.sh" ]
