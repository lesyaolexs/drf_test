setup: migrate createsuperuser
migrate:
	docker-compose -f docker-compose.yml run web ./manage.py migrate
createsuperuser:
	docker-compose -f docker-compose.yml run web ./manage.py createsuperuser --no-input

.PHONY: test
test:
	docker-compose -f docker-compose.yml run web ./manage.py test

.PHONY: db_cleanup
db_cleanup:
	docker-compose -f docker-compose.yml run web ./manage.py db_cleanup
