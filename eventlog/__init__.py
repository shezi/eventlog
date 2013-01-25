# following PEP 386
__version__ = "0.6.0"

try:
    from models import log_event, log_exception
except:
    pass
    