# no-space-alert
A very simple hardware monitoring tool

## How to run
### In a virtual environment
1. Create and activate virtual environment
2. Create and fill in `.env` file
```bash
cp .env.dist .env
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run script
```bash
make start
```

### In a docker
1. Create and fill in `.env` file
2. ...

### Development
In a new virtual environment:
- Install dependencies with `make pip-install-dev`
- If packages are updated, update dependencies with `make pip-freeze`
