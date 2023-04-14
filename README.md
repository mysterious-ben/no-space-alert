# no-space-alert
A simple tool to monitor usage of hard drive space, RAM and CPU

Output example:
```console
dev-local 2023-04-14T08:16:09.793Z INFO: hdd space on '/': used_pct=53.3 used_gb=239.41 free_gb=209.59
dev-local 2023-04-14T08:16:09.794Z INFO: hdd inodes on '/': used_pct=6.9 used=2,063,996 free=27,910,532
dev-local 2023-04-14T08:16:09.797Z INFO: ram vm_used_pct=17.5 swap_used_pct=0.0 vm_used_gb=6.03 vm_available_gb=51.54 vm_free_gb=49.21 vm_cached_gb=6.84 vm_buffers_gb=0.42 vm_total_gb=62.51 swap_free_gb=20.00 swap_used_gb=0.00 swap_total_gb=20.00
dev-local 2023-04-14T08:16:09.799Z INFO: cpu avg_pct=0.7 max_pct=1.6 min_pct=0.0 all_pct=[0.6, 0.0, 1.0, 0.6, 0.6, 0.8, 0.8, 1.0, 1.6, 0.6, 0.6, 0.4]
```

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
