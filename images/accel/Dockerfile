FROM alpine:latest

RUN apk update && apk add varnish

WORKDIR /var/lib/varnish
COPY start.sh /
RUN chmod u+x /start.sh

CMD [ "/start.sh" ]
