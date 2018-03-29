FROM alpine:latest

RUN apk update && apk add lighttpd 

RUN mkdir /var/cache/ligttpd && touch /var/log/lighttpd/lighttpd.log
COPY ./etc/* /etc/lighttpd/

RUN rm -rf /var/www/*
WORKDIR /var/www

EXPOSE 7000

CMD ["lighttpd", "-t", "-f", "/etc/lighttpd/lighttpd.conf"]
ENTRYPOINT ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
