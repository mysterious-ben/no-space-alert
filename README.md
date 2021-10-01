# no-space-alert
A very simple hardware monitoring tool

## How to run
### In a virtual environment
1. Create an `.env` file with `cp .env.dist .env`
  - List all mount paths to monitor in `MOUNT_PATHS=` (comma-separated)
  - (Optional) Set credentials for Pushover and Sentry

2. Create and activate a virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Run script with `bash make start`

### In a docker
1. Create and fill in `.env` file (see above)
2. build docker image: `docker build -t no-space-alert .`
3. docker run: `docker run -it no-space-alert make start`

## Development
In a new virtual environment:
- Install dependencies with `pip install -r requirements-dev.txt`
- If packages are updated, update dependencies with `make pip-freeze`
