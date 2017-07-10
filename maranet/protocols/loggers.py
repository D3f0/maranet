"""
Logging custom classes used in the protocols implementations
"""

import logging

class ServerLogAdapter(logging.LoggerAdapter):
    """Show server string in the logs"""
    def process(self, msg, kwargs):
        return  '[%s] %s' % ("SERVER", msg), kwargs

class COMasterLogAdapter(logging.LoggerAdapter):
    """Shows IP addresses in the logs"""
    def process(self, msg, kwargs):
        ip_address = self.extra['comaster'].ip_address
        return '[%s] %s' % (ip_address, msg), kwargs
