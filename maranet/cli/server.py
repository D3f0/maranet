import logging
import sys

import click
from twisted.internet import reactor

from maranet.mara.server import MaraServerFactory


@click.command()
@click.option('--port', default=9761)
def server(port):
    logging.basicConfig(level=logging.DEBUG)
    click.echo("Listening on port {}".format(port))
    reactor.listenTCP(port, MaraServerFactory())
    reactor.run()
