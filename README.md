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
python -m src.cli start
```

## In a docker
...