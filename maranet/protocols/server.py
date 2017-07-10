# encoding: utf-8
"""
This module emulates an embedded device.

"""
from __future__ import print_function

from copy import copy
import logging
import random
import os

from ..utils.formatters import upperhexstr
from ..constants import commands
from construct import Container
from construct.core import FieldError
from ..constructs import MaraFrame  # Event
from twisted.internet import protocol
from ..utils.formatters import hexstr2buffer
import logging
from .loggers import ServerLogAdapter

random.seed(os.getpid())

logger = ServerLogAdapter(logging.getLogger(__name__), {})

def random_bytes(count):
    """
    Mara aware value generator. Creates the Mara offset and values
    :returns (offset, data)
    """
    return (count+1, [random.randrange(0, 0xFF) for x in xrange(count)])


def random_words(count):
    """
    Mara aware value generator. Creates the Mara offset and values
    :returns (offset, data)
    """
    return ((count*2)+1, [random.randrange(0, 0xFFFF) for x in range(count)])


class MaraServer(protocol.Protocol):
    """
    Works as COMaster development board
    It replies commands 0x10 based on the definition
    in the comaster instance (a DB table).
    """

    def connectionMade(self,):
        logger.debug("Conection made to %s:%s" % self.transport.client)
        self.input = Container()
        self.output = None
        self.last_seq = None
        self.last_peh = None
        self.peh_count = 0

    def sendContainer(self, container):
        """Convenience method for publishing when data is sent"""
        assert isinstance(container, Container)
        data = self.construct.build(container)
        logger.info("Reponding -> %s", upperhexstr(data))
        self.transport.write(data)

    def dataReceived(self, data):
        try:
            self.input = MaraFrame.parse(data)
            self.maraPackageReceived()
        except FieldError:
            # If the server has no data, it does not matter
            self.input = None
            logger.warn("Error de pareso: %s" % upperhexstr(data))

    def maraPackageReceived(self):
        """Note: Input holds input package parse results"""
        if self.input.command == 0x10:
            # Response for command 0x10
            logger.info("Responding Mara Frame from: %s", self.transport)
            if self.input.sequence == self.last_seq and self.output:
                logger.debug("Sending same package!")
            else:
                self.last_seq = self.input.sequence
                self.output = self.buildPollResponse()
            self.sendContainer(self.output)
        elif self.input.command == commands.PEH.value:

            logger.info("PEH: %s", self.input.peh)
        else:
            logger.warning("Not responding to package %x", self.input.command)

    def buildPollResponse(self):
        """It should reassemble what the COMaster does"""

        output = copy(self.input)
        # exchange input
        output.source, output.dest = self.input.dest, self.input.source
        # show current squence number
        logger.info("Sequence: %d", self.input.sequence)

        canvarsys, varsys = random_bytes(self.factory.sv_count*2)
        candis, dis = random_words(self.factory.di_count)
        canais, ais = random_words(self.factory.ai_count)
        output.payload_10 = Container(
            canvarsys=canvarsys,
            varsys=varsys,
            candis=candis,
            dis=dis,
            canais=canais,
            ais=ais,
            event=[],
            canevs=1,
        )
        return output

    def sendFixedRespose(self):

        bad_data = (
            'FE 08 0A 01 06 10 F1 E6 19 16 2D 2A 00 40 01 A4 50 00 00 00 00 00 00 00 00'
            '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
            '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
            '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
            '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
            '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
        )

        self.transport.write(hexstr2buffer(bad_data))

    def connectionLost(self, reason):
        logger.info("Connection with %s: %s", self.transport.client, reason)

class MaraServerFactory(protocol.Factory):
    protocol = MaraServer

    di_count = 16
    ai_count = 6
    sv_count = 6

    def buildProtocol(self, addr):
        logger.info("Building protocol for %s", addr)
        proto = protocol.Factory.buildProtocol(self, addr)
        proto.construct = MaraFrame
        return proto
