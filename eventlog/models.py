from datetime import datetime
import traceback

from django.db import models

from django.contrib.auth.models import User

import jsonfield

import logging
logger = logging.getLogger('eventlog')


class Event(models.Model):
    """A simple event logging model."""
    
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    level = models.IntegerField()
    label = models.CharField(max_length=50)
    message = models.TextField(null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    extra = jsonfield.JSONField(null=True)
    
    class Meta:
        ordering = ["-timestamp"]

def create_event(label, message=None, user=None, extra=None, level=logging.INFO, django_log=True):
    """Create/log an event that has happened and attach the given information to it.
    
    label fills the `label` field in the model.
    message fills the `message` field in the model.
    user filles the `user` field in the model.
    extra fills the `extra` field in the model.
    level filles the `level` field in the model and determines the loglevel for the Django logging system if necessary
    django_log determines whether the event should be passed on to the regular Django logging stream
    """
    if user is not None and not user.is_authenticated():
        user = None

    event = Event.objects.create(label=label, user=user, message=message, level=level, extra=extra)
    
    if django_log:
        logger.log(level, "{id:016} {label} {user}- {message}{extra}".format(
            label=label,
            user = "(user: {0}) ".format(user.username) if user else "",
            message = message + " " if message else "",
            extra=extra or "",
            id=event.id
        ))
        
    return event


def log_debug(label, message=None, user=None, extra=None, django_log=True):
    """Log an event at the debug level.
    
    Don't overuse this!
    """
    return create_event(label, message, user, extra, logging.DEBUG, django_log)


def log_info(label, message=None, user=None, extra=None, django_log=True):
    """Log an event that has happened and attach extra information to it."""
    return create_event(label, message, user, extra, logging.INFO, django_log)
log_event = log_info


def log_warning(label, message=None, user=None, extra=None, django_log=True):
    """Log an event that has happened and attach extra information to it."""
    return create_event(label, message, user, extra, logging.WARNING, django_log)


def log_error(label, message=None, user=None, extra=None, django_log=True):
    """Log an event that has happened and attach extra information to it."""
    return create_event(label, message, user, extra, logging.ERROR, django_log)


def log_fatal(label, message=None, user=None, extra=None, django_log=True):
    """Log a fatal event.
    
    Note that, since we're trying to access the database, the event log might not make it through.
    """
    try:
        event = create_event(label, message, user, extra, logging.ERROR, django_log=false)
    except:
        event = None
        
    if django_log:
        logger.fatal("{label} {user}- {message}{extra}".format(
            label=label,
            user = "(user: {0}) ".format(user.username) if user else "",
            message = message + " " if message else "",
            extra=extra or "",
        ))
        
    return event


def log_exception(label, message=None, user=None, extra=None, level=logging.WARNING, django_log=True):
    """Log an exception that occurred in your code.
    
    Call this only during a catch block! Because we have to retrieve the exception info from sys, it might be cleared
    if you are not in the catch block any more
    
    This will format the exception nicely, put it in extra['exception'] and log it as an event with given level.
    """
    if extra is None:
        extra = {}
    
    # funny how this is _so_ not functional, isn't it?
    exception = traceback.format_exc()
    extra['exception'] = exception
    
    return create_event(label, message, user, extra, level, django_log)
    
