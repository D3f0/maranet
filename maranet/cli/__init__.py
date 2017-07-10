"""
Command line interfase
"""
import click
from .server import server
from .client import direct_poll, client


@click.group()
def cli():
    pass

cli.add_command(client)
cli.add_command(server)
cli.add_command(direct_poll)
