=======
MaraNet
=======


.. image:: https://img.shields.io/pypi/v/maranet.svg
        :target: https://pypi.python.org/pypi/maranet

.. image:: https://img.shields.io/travis/D3f0/maranet.svg
        :target: https://travis-ci.org/D3f0/maranet

.. image:: https://readthedocs.org/projects/maranet/badge/?version=latest
        :target: https://maranet.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/D3f0/maranet/shield.svg
     :target: https://pyup.io/repos/github/D3f0/maranet/
     :alt: Updates


A Python client library for MARA protocol. Includes server emulator, although MARA servers are tipically microcontrollers.


* Free software: MIT license
* Documentation: https://maranet.readthedocs.io.


Mara Network Protocol
=====================


Mara is a protocol designed for interaction with a network of embedded devices.
These devices collect state and events from a process (implementations include
traffic light systems and power station monitoring).

Mara 1.0 is source code is implemented on top of Microchip PIC devices and code
can be requested at ricadoalopez at gmail.

Mara 1.6, designed with 16 bit in mind, is implemented on top of Arduino libraries and
should be available soon.


Mara 1.0
--------

Mara packages structure::

    ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐┌─────┐┌─────┬─────┐
    │ SOF │ SEQ │ QTY │ SRC │ DST │ CMD │ PLD ││ ... ││ BCL │ BCH │
    │     │     │     │     │     │     │     ││     ││     │     │
    └─────┴─────┴─────┴─────┴─────┴─────┴─────┘└─────┘└─────┴─────┘
    ┌─────┬───────────┬───────────┬─────┬───────────┬───────────┐
    │ QSV │ SV0       │ SV1       │ QDI │ DI0       │ DI1       │
    │     │           │           │     │           │           │
    └─────┴───────────┴───────────┴─────┴───────────┴───────────┘
    ┌─────┬───────────┬───────────┬─────┬─────────────────────────┐
    │ QAI │ AI0       │ AI1       │ QEV │ EV..                    .
    │     │           │           │     │                         │
    └─────┴───────────┴───────────┴─────┴─────────────────────────┘

Where:

    * **SOF** Start of frame
    * **SEQ** Sequence number
    * **QTY** Frame length or byte *quantity*
    * **SRC** Source address
    * **DST** Destination address
    * **CMD** Command
    * **PLD** Payload
        - Payload consists of arrays of values

