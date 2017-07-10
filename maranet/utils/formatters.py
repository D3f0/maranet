"""
Conversion functions
"""
import re
import os
import binascii
import jinja2
from copy import copy


def upperhexstr(buff):
    """Buffer -> Upper Human Readable Hex String"""
    return ' '.join([("%.2x" % ord(c)).upper() for c in buff])


def ints_from_str(hexstr):
    '''Takes ints from hexstring

    >>> input_string = 'FE    08    01    40    80    10    80    A7'
    >>> list(ints_from_str(input_string))
    [0xFE, 0x08, 0x01, 0x40, 0x80, 0x10, 0x80, 0xA7]
    '''
    parts = re.split(r'[\s:\t]', hexstr)
    for part in filter(len, parts):
        yield int(part, 16)

def format_buffer(buff):
    '''Buffer to human readable hex representation'''
    bytes_in_hex = " ".join(("%.2x" % one_byte for one_byte in map(ord, buff)))
    return bytes_in_hex.upper()

def hexstr2buffer(hex_text_with_spaces):
    hex_text_without_spaces = hex_text_without_spaces.replace(' ', '')
    return binascii.unhexlify(hex_text_without_spaces)


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
)


env.filters['upperhex'] = lambda an_int: type(an_int) is not int and "??" or ('%.2x' % an_int).upper()

def format_frame(frame,
        as_hex_string=False,
        show_header=True,
        show_di=True,
        show_ai=True,
        show_sv=True,
        show_ev=True,
        show_bcc=True):
    '''Foramts Mara frame for human inspection'''
    context = copy(locals())
    template = env.get_template('frame.j2')
    return template.render(**context)

def print_frmae(*args, **kwargs):
    print(format_frame(*args, **kwargs))
