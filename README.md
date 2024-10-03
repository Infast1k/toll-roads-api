# API for Toll Roads application

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/your_repository.git &&
   cd your_repository
   ```

2. Install all required packages in `Requirements` section.


### Implemented Commands
* `make app` - up application and all infrastructure
* `make app-down` - down application and all infrastructure
* `make logs` - follow the logs in all containers
* `make api-logs` - follow the logs in api container
* `make api-exec` - exec bash shell in api container
* `make pg-logs` - follow the logs in postgres container
* `make redis-logs` - follow the logs in redis container

### Most Used Django Specific Commands

* `make migr` - apply all made migrations
* `make make-migr` - make migrations to models
* `make superuser` - create admin user
