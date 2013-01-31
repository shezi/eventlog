# following PEP 386
__version__ = "0.7.0"

try:
    from models import create_event
    from models import log_debug, log_info, log_event, log_warning, log_error, log_fatal
    from models import log_exception
except:
    pass
    