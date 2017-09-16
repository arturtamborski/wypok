images = proxy static accel app cache db broker

all: prepare build run

run:
	@docker-compose -f images/docker-compose.yaml up

build: prepare
	@docker-compose -f images/docker-compose.yaml build

clean: stop
	-@rm -I -rf logs/ volumes/

rmi: stop
	-@docker rmi $(images)

stop:
	-@docker-compose -f images/docker-compose.yaml rm -f

prepare: $(images)

$(images): %: logs/% volumes/%

logs/%: logs
	-@mkdir -p $@

volumes/%: volumes
	-@mkdir -p $@

logs volumes:
	-@mkdir -p $@

.PHONY: all run clean rmi stop prepare
