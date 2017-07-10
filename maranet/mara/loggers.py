import logging
class ServerLogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return  '[%s] %s' % ("SERVER", msg), kwargs
