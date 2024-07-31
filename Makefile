DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs -f
API_CONTAINER = toll-roads-api
POSTGRES_CONTAINER = toll-roads-postgres

.PHONY: app
app:
	${DC} up --build -d

.PHONY: app-down
app-down:
	${DC} down

.PHONY: api-logs
api-logs:
	${LOGS} ${API_CONTAINER}

.PHONY: api-exec
api-exec:
	${EXEC} ${API_CONTAINER} bash

.PHONY: makemigrations
makemigrations:
	${EXEC} ${API_CONTAINER} python3 manage.py makemigrations

.PHONY: migrate
migrate:
	${EXEC} ${API_CONTAINER} python3 manage.py migrate

.PHONY: superuser
superuser:
	${EXEC} ${API_CONTAINER} python3 manage.py createsuperuser

.PHONY: pg-logs
pg-logs:
	${LOGS} ${POSTGRES_CONTAINER}