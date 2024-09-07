DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
MANAGE_PY = python manage.py
API_CONTAINER = toll-roads-api
POSTGRES_CONTAINER = toll-roads-postgres

.PHONY: app
app:
	${DC} up --build -d

.PHONY: app-down
app-down:
	${DC} down

.PHONY: logs
logs:
	${DC} logs -f

.PHONY: api-logs
api-logs:
	${LOGS} ${API_CONTAINER} -f

.PHONY: api-exec
api-exec:
	${EXEC} ${API_CONTAINER} /bin/bash

.PHONY: pg-logs
pg-logs:
	${LOGS} ${POSTGRES_CONTAINER} -f

.PHONY: migr
migr:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: make-migr
make-migr:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser