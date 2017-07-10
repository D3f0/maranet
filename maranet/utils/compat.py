"""
Functions for automatic configuration based on Django settings.
"""

import logging
from importlib import import_module

logger = logging.getLogger(__name__)

def get_setting(name, default=None):
    """
    Tries to get settings from Django
    """
    try:
        from django.conf import settings
        return getattr(settings, name, default)
    except ImportError:
        logger.warn("Could not get setting {}".format(name))
    return default

def import_class(module_dot_class):
    '''Given a class name returns the calss reference'''
    module_name, class_name = module_dot_class.rsplit('.', 1)
    module = import_module(module_name)
    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError('Module %s has no %s' % (module_name, class_name))
