FROM postgres:9.6.4-alpine

COPY ./etc/* /etc/postgresql/
COPY ./init/* /docker-entrypoint-initdb.d/
