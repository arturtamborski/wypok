FROM alpine:latest

RUN apk update && apk add lighttpd 

RUN mkdir /var/cache/ligttpd && touch /var/log/lighttpd/lighttpd.log
COPY lighttpd.conf /etc/lighttpd/lighttpd.conf

RUN rm -rf /var/www/*
WORKDIR /var/www

RUN ["lighttpd", "-t", "-f", "/etc/lighttpd/lighttpd.conf"]
ENTRYPOINT ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
