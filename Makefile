DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs -f
API_CONTAINER = toll-roads-api

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
