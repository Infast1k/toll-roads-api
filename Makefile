DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
MANAGE_PY = python manage.py
API_CONTAINER = toll-roads-api
POSTGRES_CONTAINER = toll-roads-postgres
REDIS_CONTAINER = toll-roads-redis

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

.PHONY: redis-logs
redis-logs:
	${LOGS} ${REDIS_CONTAINER} -f

.PHONY: migr
migr:
	${EXEC} ${API_CONTAINER} ${MANAGE_PY} migrate

.PHONY: make-migr
make-migr:
	${EXEC} ${API_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${API_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: test
test:
	${EXEC} ${API_CONTAINER} ${MANAGE_PY} test