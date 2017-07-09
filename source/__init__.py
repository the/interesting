import logging, re

def name_from_module(module):
    return re.sub('source\.([a-zA-Z0-9_]+)\..+', r'\1', module)

def get_logger(module):
    return logging.getLogger(name_from_module(module))
