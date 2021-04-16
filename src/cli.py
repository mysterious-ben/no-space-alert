import click

from src import alarms


@click.group()
def cli():
    pass


@click.command()
def start():
    alarms.start()


cli.add_command(start)

if __name__ == "__main__":
    cli()
