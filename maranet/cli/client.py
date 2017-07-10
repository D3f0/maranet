'''
Poll UC directly
Show how to make direct poll of COMaster
'''

import click
from socket import socket, error
from maranet.constructs import MaraFrame
from construct.lib.container import Container
from time import sleep
from construct.core import FieldError
from maranet import constants
from maranet.utils.formatters import format_frame
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

def timestamp_str():
    """Shows timestamp"""
    now = datetime.now()
    return now.strftime("%X us:") + "%d" % now.microsecond


log_levels = click.Choice([
 'DEBUG',
 'INFO',
 'ERROR',
 'WARNING'
 'CRITICAL',
 'FATAL',
])

@click.command()
@click.option('--port', default=9761)
@click.option('--host', default='127.0.0.1')
@click.option('--interval', default=1, type=float)
@click.option('--log', default='INFO', type=log_levels)
@click.option('--dis/--no-dis', default=True, help="Show mara DI")
@click.option('--ais/--no-ais', default=True, help="Show mara AI")
@click.option('--svs/--no-svs', default=False, help="Show mara System Variables")
@click.option('--evts/--no-evts', default=True, help="Shoe mara events")
def direct_poll(port, host, interval, log, dis, ais, svs, evts):
    """
    Direct poll, uses plain socket and consturcts to encode/decode mara.
    """
    logging.basicConfig(level=getattr(logging, log))

    try:
        interval = float(interval)
    except ValueError as e:
        click.echo(e, file='stderr')

    conn = socket()
    try:
        conn.connect((host, port))
    except error as e:
        logger.critical("{} {}:{}".format(host, port, e))
        return
    output = Container(
        source=64,
        dest=1,
        sequence=constants.sequence.MIN.value,
        command=0x10,
        payload_10=None
    )

    while True:
        logging.info(timestamp_str())
        pkg = MaraFrame.build(output)
        conn.send(str(pkg))
        # Block until reply
        data = conn.recv(1024)
        try:
            data = MaraFrame.parse(data)
        except FieldError as e:
            click.echo("Error decoding frame: {}".format(e))
            continue

        logger.info(
            format_frame(data,
                show_header=True,
                show_bcc=False,
                # Flags
                show_di=dis,
                show_ai=ais,
                show_sv=svs,
                show_ev=evts
            )
        )
        sleep(interval)
        output.sequence += 1
        if output.sequence > constants.sequence.MAX.value:
            output.sequence = constants.sequence.MIN.value

@click.command()
@click.option('--port', default=9761)
@click.option('--host', default='127.0.0.1')
@click.option('--interval', default=1, type=float)
def client(port, host, interval):
    """
    Twisted based client
    """
    pass
