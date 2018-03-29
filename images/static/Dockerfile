FROM alpine:latest

RUN apk update && apk add lighttpd 

COPY ./etc/* /etc/lighttpd/

WORKDIR /var/www

EXPOSE 7000

CMD ["lighttpd", "-t", "-f", "/etc/lighttpd/lighttpd.conf"]
ENTRYPOINT ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
