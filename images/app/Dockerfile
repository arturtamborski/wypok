FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

COPY run.sh /
COPY ./etc/repositories /etc/apk/repositories
COPY ./etc/* /etc/wypok/

# libs for libmagic, psycopg2 and pillow from requirements.txt
RUN apk update && \
	apk add postgresql-dev gcc python3-dev musl-dev freetype-dev libmagic \
	lcms2-dev libjpeg-turbo-dev libwebp-dev openjpeg-dev tiff-dev zlib-dev

# libmagic won't find itself if it has numbers after extension
RUN ln -s /usr/lib/libmagic.so.1 /usr/lib/libmagic.so

# install dependencies
RUN pip install -r /etc/wypok/requirements.txt

WORKDIR /app

EXPOSE 8000

ENTRYPOINT [ "sh", "/run.sh" ]
