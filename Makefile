NAME =	moul/readthedocs

build:
	docker build -t $(NAME) .

release:
	docker push $(NAME)

run:
	docker-compose run --service-ports --rm readthedocs
debug-run:
	docker-compose run --service-ports --rm readthedocs bash
debug-app:
	docker exec -ti dockerreadthedocs_readthedocs_run_9 bash
