FROM redis:4-alpine

RUN mkdir /etc/redis
COPY ./redis.conf /etc/redis/redis.conf

#ENTRYPOINT ["docker-entrypoint.sh", "/etc/redis/redis.conf"]

CMD ["redis-server", "/etc/redis/redis.conf"]
