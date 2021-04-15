# no-space-alert
A very simple hardware monitoring tool

## How to run
### Use a virtual environment
1. Сreate and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

2. Create /.env

```bash
SPACE_LIMIT_WARNING=<Max size in GB for warning>
SPACE_LIMIT_ERROR=<Max size in GB for error>
CHECK_PERIOD=<Period in second to repeat schedule>
MOUNT_PATH=<disk mount for monitoring>
```
example:

```.env
SPACE_LIMIT_WARNING=3
SPACE_LIMIT_ERROR=2
CHECK_PERIOD=5
MOUNT_PATH=/
```

3. Install dependencies
```bash
pip install -r venv_requirements.txt
```
