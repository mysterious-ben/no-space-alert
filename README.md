# no-space-alert
A simple monitoring tool for hard drive space and RAM

## Installation
Clone this GitHub repository.

## How to run
### In a virtual environment
1. Create an `.env` file with `cp .env.dist .env`
  - List paths to monitor in `MOUNT_PATHS=` (comma-separated)
  - List file systems to monitor in `FILE_SYSTEMS=` (comma-separated; only used if `MOUNT_PATHS` is empty)
  - (Optional) Set credentials for Pushover, Slack and Sentry

2. Create and activate a virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Run script with `bash make start`

### In a docker
1. Create and fill in `.env` file (see above)
  - Also set paths in `DOCKER_MOUNT_PATH_{N}=` to make them visible to docker (apart from `/`)
2. build docker image: `docker build -t no-space-alert .`
3. docker run: `docker run -it no-space-alert make start`

## Development
In a new virtual environment:
- Install dependencies with `pip install -r requirements-dev.txt`
- If packages are updated, update dependencies with `make pip-freeze`
