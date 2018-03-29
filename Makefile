images = proxy static accel app cache db broker

run:
	@docker-compose -f images/docker-compose.yaml up

all: prepare build run

build: prepare
	@docker-compose -f images/docker-compose.yaml build

clean: stop
	-@rm -I -rf logs/ volumes/

rmi: stop
	-@docker rmi $(images)

stop:
	-@docker-compose -f images/docker-compose.yaml rm -f

manage:
	docker exec -it app sh /run.sh $(MAKECMDGOALS)

prepare: $(images)

$(images): %: logs/% volumes/%

logs/%: logs
	-@mkdir -p $@

volumes/%: volumes
	-@mkdir -p $@

logs volumes:
	-@mkdir -p $@

.PHONY: all run clean rmi stop prepare manage
