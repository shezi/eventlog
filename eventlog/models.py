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
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)
    extra = jsonfield.JSONField()
    
    class Meta:
        ordering = ["-timestamp"]


def log_event(action, user=None, extra=None, loglevel=logging.INFO):
    """Log an event that has happened and attach extra information to it.
    
    If a loglevel is given, the event will additionally be logged through the standard Django logging system at that
    level. If you do __not__ want to log, set loglevel=None.
    """
    if user is not None and not user.is_authenticated():
        user = None
    if extra is None:
        extra = {}
    
    if loglevel is not None:
        if user:
            logger.log(loglevel, "%s (user %s) - %s" % (action, user.username, str(extra)))
        else:
            logger.log(loglevel, "%s - %s" % (action, str(extra)))
    
    return Event.objects.create(user=user, action=action, extra=extra)

def log_exception(action, user=None, extra=None, loglevel=logging.WARNING):
    """Log an exception that occurred in your code.
    
    Call this only during a catch block! Because we have to retrieve the exception info from sys, it might be cleared
    if you are not in the catch block any more
    
    This will format the exception nicely, put it in extra['exception'] and log it as an event with loglevel.
    """
    if extra is None:
        extra = {}
    
    # funny how this is so not functional, isn't it?
    exception = traceback.format_exc()
    extra['exception'] = exception
    
    log_event(action, user, extra, loglevel)